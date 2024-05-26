import math
from typing import Any

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound

from model.creation_table import *

type userType = {"id": int, "name": str, "passwd": str}
userConnect: userType = {"id": None, "name": "", "passwd": ""}

# Création et utilisation d'une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()


def addUser(name: str, passwd: str, email: str = "") -> bool:
    try:
        result = session.query(Users).filter(Users.username == name).one()
        print("user already existed ! ")
        return False
    except NoResultFound:
        new_user = Users(name=name, password=passwd, email=email)
        session.add(new_user)
        session.commit()
        print("user created successfully ! ")
        return True


def connectUser(name: str, passwd: str, email: str = "") -> bool:
    global userConnect
    try:
        result = session.query(Users).filter(and_(Users.name == name,
                                                  Users.password == passwd)).one()
        if result:
            userConnect["id"] = result.id_user
            userConnect["name"] = result.name
            userConnect["passwd"] = result.password
            print(f"user {name} logged in successfully !")
            return True
    except NoResultFound:
        print(f'there is no account for username {name} and password {passwd}')
        return False


def disconnectUser() -> bool:
    global userConnect
    if userConnect["id"] is not None:
        userConnect["id"] = None
        userConnect["name"] = ""
        userConnect["passwd"] = ""
        print(f"user logged out successfully !")
        return True
    return False


def searchFlight(type_seat: str, date_dep: str = "", date_arr: str = "",
                 country_dep:
                 str = "",
                 country_arr: str = "",
                 price: float = math.inf, cmp: str = "equals") -> Any:
    result = session.query(Flight, Procure, Classe, Price, Provider).join(
        Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                            Procure.id_Classe
                                                            ==
                                                            Classe.id_Classe).join(
        Price, Price.id_price == Procure.id_price).join(Provider,
                                                        Provider.id_provider == Procure.id_provider)

    if type_seat != "":
        result = result.filter(Classe.name_Classe == type_seat)

    if date_dep != "":
        result = result.filter(Flight.date_dep == date_dep)

    if date_arr != "":
        result = result.filter(Flight.date_arr == date_arr)

    if country_dep != "":
        result = result.filter(Flight.country_dep == country_dep)

    if country_arr != "":
        result = result.filter(Flight.country_arr == country_arr)

    if price != math.inf:
        if cmp == "equals":  # if cmp is '=', then we filter the flight based on the equals price given in parameters
            result = result.filter(Price.price == price)
        elif cmp == "inf":  # if cmp is '<', then we filter the flight based on the lower price given in parameters
            result = result.filter(Price.price < price)
        elif cmp == "infequals":  # if cmp is '<=', then we filter the flight
            # based on the equals or lower price given in parameters
            result = result.filter(Price.price <= price)
        elif cmp == "supequals":  # if cmp is '>=', then we filter the flight
            # based on the equals or upper price given in parameters
            result = result.filter(Price.price >= price)
        elif cmp == "sup":  # if cmp is '>', then we filter the flight based on the upper price given in parameters
            result = result.filter(Price.price > price)
        else:  # that sign of cmp is not recognized !
            print("I don't recognize that value of cmp for this research !")

    if (
            country_dep == "" and country_arr == "" and type_seat == "" and price
            == math.inf and date_dep == "" and date_arr == ""):
        result = session.query(Flight, Procure, Classe, Price, Provider).join(
            Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                                Procure.id_Classe
                                                                ==
                                                                Classe.id_Classe).join(
            Price, Price.id_price == Procure.id_price).join(Provider,
                                                            Provider.id_provider == Procure.id_provider).all()
    else:
        result = result.all()

    if result:
        line_format = (
            "| {:<14} | {:<14} | {:<14} | {:<14} | {:<14} | {:<12} | {}")
        print(line_format.format("name_provider", "country_dep", "country_arr",
                                 "date_dep", "date_arr", "Classe", "price"))

        for flight, provider, classe, price in result:
            print(line_format.format(provider.name_provider,
                                     flight.country_dep, flight.country_arr,
                                     flight.date_dep, flight.date_arr,
                                     classe.name_class, price.price_value))

    else:
        print("there is no records found for your request !")



def bookFlight():
