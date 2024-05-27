import math
from datetime import datetime
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
        result = session.query(Users).filter(Users.name == name).one()
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


def searchFlight(type_seat: str = "", date_dep: str = "", date_arr: str = "",
                 country_dep:
                 str = "",
                 country_arr: str = "",
                 price: float = math.inf, cmp: str = "equals", provider_name: str = "") -> Any:
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

    if provider_name != "":
        result = result.filter(Provider.name_provider == provider_name)

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
            == math.inf and date_dep == "" and date_arr == "" and provider_name == ""):
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


def bookFlight(classe: str, idflight: int, providername: str) -> str:
    global userconnect

    if userConnect["id"] is None:
        print("You need login to proceed")
        return "You need login to proceed"
    try:
        # Recherche du vol
        flight = session.query(Flight).filter(Flight.id_flight == idflight).first()
        if not flight:
            return "Le vol n'existe pas."

        # Recherche du fournisseur
        provider = session.query(Provider).filter(Provider.name_provider == providername).first()
        if not provider:
            return "Le fournisseur n'existe pas."

        # Vérification de la relation flight-provider-class
        procure = session.query(Procure).filter(
            Procure.id_flight == idflight,
            Procure.id_provider == provider.id_provider,
            Procure.class_.has(name_class=classe)
        ).first()

        if not procure:
            return "Le fournisseur ne propose pas cette classe pour ce vol."

        # Vérification de la disponibilité des sièges
        class_capacity = procure.class_.capacity
        current_bookings = session.query(Book).filter(
            Book.id_flight == idflight,
            Book.id_class == procure.class_.id_class
        ).count()

        if current_bookings >= class_capacity:
            return f"Pas de sièges disponibles en classe {classe}."

        # Création de la réservation
        new_booking = Book(
            flight_number=current_bookings + 1,
            date_book=datetime.date.today(),
            id_price=procure.id_price,
            id_class=procure.id_class,
            id_flight=idflight,
            id_user=userConnect["id"]
        )

        session.add(new_booking)
        session.commit()
        print(f"Réservation réussie en classe {classe} pour le vol {idflight} avec {providername}.")
        return f"Réservation réussie en classe {classe} pour le vol {idflight} avec {providername}."
    except NoResultFound:
        return "Erreur lors de la réservation : données introuvables."
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la réservation : {str(e)}")
        return f"Erreur lors de la réservation : {str(e)}"



# bookFlight("Economy", 1, "Air France")

