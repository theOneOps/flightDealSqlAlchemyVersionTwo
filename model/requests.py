import datetime
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
        result = session.query(Users).filter(Users.name == name).one()
        print("user already existed ! ")
        return False
    except NoResultFound:
        new_user = Users(name=name, password=passwd, email=email)
        session.add(new_user)
        session.commit()
        print("user created successfully ! ")
        return True


# addUser("rohn", "lid", "rohnlid@gmail.com")


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

def isUserConnected()->bool:
    global userConnect
    if userConnect["id"] is not None:
        return True
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


# disconnectUser()

def searchFlight(type_seat: str = "", date_dep: str = "", date_arr: str = "",
                 country_dep:
                 str = "",
                 country_arr: str = "",
                 price: float = math.inf, cmp: str = "equals",
                 provider_name: str = "") -> Any:
    result = session.query(Flight, Procure, Classe, Price, Provider).join(
        Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                            Procure.id_class
                                                            ==
                                                            Classe.id_class).join(
        Price, Price.id_price == Procure.id_price).join(Provider,
                                                        Provider.id_provider == Procure.id_provider)

    if type_seat != "":
        result = result.filter(Classe.name_class == type_seat)

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
            result = result.filter(Price.price_value == price)
        elif cmp == "inf":  # if cmp is '<', then we filter the flight based on the lower price given in parameters
            result = result.filter(Price.price_value < price)
        elif cmp == "infequals":  # if cmp is '<=', then we filter the flight
            # based on the equals or lower price given in parameters
            result = result.filter(Price.price_value <= price)
        elif cmp == "supequals":  # if cmp is '>=', then we filter the flight
            # based on the equals or upper price given in parameters
            result = result.filter(Price.price_value >= price)
        elif cmp == "sup":  # if cmp is '>', then we filter the flight based on the upper price given in parameters
            result = result.filter(Price.price_value > price)
        else:  # that sign of cmp is not recognized !
            print("I don't recognize that value of cmp for this research !")

    if (
            country_dep == "" and country_arr == "" and type_seat == "" and price
            == math.inf and date_dep == "" and date_arr == "" and provider_name == ""):
        result = session.query(Flight, Procure, Classe, Price, Provider).join(
            Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                                Procure.id_class
                                                                ==
                                                                Classe.id_class).join(
            Price, Price.id_price == Procure.id_price).join(Provider,
                                                            Provider.id_provider == Procure.id_provider).all()
    else:
        result = result.all()

    if result:
        line_format = (
            "| {:<18} | {:<20} | {:<20} | {:<18} | {:<20} | {:<20} | {}")
        print(line_format.format("name_provider", "country_dep", "country_arr",
                                 "date_dep", "date_arr", "classe", "price"))

        for flight, procure, classe, price, provider in result:
            print(line_format.format(provider.name_provider,
                                     flight.country_dep, flight.country_arr,
                                     str(flight.date_dep), str(flight.date_arr),
                                     classe.name_class, price.price_value))

    else:
        print("there is no records found for your request !")

    return result


# searchFlight()
# searchFlight(provider_name="Air France")

def bookFlight(classe: str, idflight: int, providername: str) -> str:
    global userconnect

    if userConnect["id"] is None:
        print("You need login to proceed")
        return "You need login to proceed"
    try:
        # Recherche du vol
        flight = session.query(Flight).filter(
            Flight.id_flight == idflight).first()
        if not flight:
            return "Le vol n'existe pas."

        # Recherche du fournisseur
        provider = session.query(Provider).filter(
            Provider.name_provider == providername).first()
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
        print(
            f"Réservation réussie en classe {classe} pour le vol {idflight} avec {providername}.")
        return f"Réservation réussie en classe {classe} pour le vol {idflight} avec {providername}."
    except NoResultFound:
        return "Erreur lors de la réservation : données introuvables."
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la réservation : {str(e)}")
        return f"Erreur lors de la réservation : {str(e)}"


def searchBook(type_seat: str = "", date_dep: str = "", date_arr: str = "",
               date_book: str = "",
               country_dep:
               str = "",
               country_arr: str = "",
               price: float = math.inf, cmp: str = "equals",
               provider_name: str = ""):
    global userConnect

    if userConnect["id"] is not None:

        result = (session.query(Flight, Procure, Classe, Price, Provider,
                                Book).join(
            Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                                Procure.id_class
                                                                ==
                                                                Classe.id_class).join(
            Price, Price.id_price == Procure.id_price).join(Provider,
                                                            Provider.id_provider == Procure.id_provider)
        .join(Book, Book.id_flight == Flight.id_flight).filter(
            Book.id_user == userConnect["id"]))

        if type_seat != "":
            result = result.filter(Classe.name_class == type_seat)

        if date_dep != "":
            result = result.filter(Flight.date_dep == date_dep)

        if date_arr != "":
            result = result.filter(Flight.date_arr == date_arr)

        if date_book != "":
            result = result.filter(Book.date_book == date_book)

        if country_dep != "":
            result = result.filter(Flight.country_dep == country_dep)

        if country_arr != "":
            result = result.filter(Flight.country_arr == country_arr)

        if provider_name != "":
            result = result.filter(Provider.name_provider == provider_name)

        if price != math.inf:
            if cmp == "equals":  # if cmp is '=', then we filter the flight based on the equals price given in parameters
                result = result.filter(Price.price_value == price)
            elif cmp == "inf":  # if cmp is '<', then we filter the flight based on the lower price given in parameters
                result = result.filter(Price.price_value < price)
            elif cmp == "infequals":  # if cmp is '<=', then we filter the flight
                # based on the equals or lower price given in parameters
                result = result.filter(Price.price_value <= price)
            elif cmp == "supequals":  # if cmp is '>=', then we filter the flight
                # based on the equals or upper price given in parameters
                result = result.filter(Price.price_value >= price)
            elif cmp == "sup":  # if cmp is '>', then we filter the flight based on the upper price given in parameters
                result = result.filter(Price.price_value > price)
            else:  # that sign of cmp is not recognized !
                print("I don't recognize that value of cmp for this research !")

        if (
                country_dep == "" and country_arr == "" and type_seat == "" and price
                == math.inf and date_dep == "" and date_arr == "" and
                provider_name == "" and date_book == ""):
            result = (session.query(Flight, Procure, Classe, Price, Provider,
                                    Book
                                    ).join(
                Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                                    Procure.id_class
                                                                    ==
                                                                    Classe.id_class).join(
                Price, Price.id_price == Procure.id_price).join(Provider,
                                                                Provider.id_provider == Procure.id_provider).join(
                Book, Book.id_flight == Flight.id_flight)
                      .filter(Book.id_user == userConnect["id"]).all())
        else:
            result = result.all()

        if result:
            line_format = (
                "|{:<20} | {:<20} | {:<18} | {:<20} | {:<20} | {:<18} | {"
                ":<20} | {:<20} | {}")
            print(line_format.format("flight_number", "date of book",
                                     "name_provider",
                                     "country_dep",
                                     "country_arr",
                                     "date_dep", "date_arr", "classe", "price"))

            for flight, procure, classe, price, provider, book in result:
                print(line_format.format(book.flight_number,
                                         str(book.date_book),
                                         provider.name_provider,
                                         flight.country_dep, flight.country_arr,
                                         str(flight.date_dep),
                                         str(flight.date_arr),
                                         classe.name_class, price.price_value))

        else:
            print("there is no records found for your request !")
        return result
    else:
        raise Exception("you should be connect first")


# addUser("johndoe", "azerty")
#connectUser("johndoe", "azerty")

#searchBook()


# bookFlight("Economy", 1, "Air France")

# def cancelBook(id_flight: int, id_book:int, class_name:str, provider_name:str)

## now the utility functions

def getResultsFrom(result, books: bool = True) -> dict[str, list]:
    l: dict[str, list] = {}
    if books:
        l = {
            "price": [""],
            "country_dep": [""],
            "country_arr": [""],
            "date_dep": [""],
            "date_arr": [""],
            "provider_name": [""],
            "id_vol": [""],
            "capacity_left": [],
        }
    else:
        l = {
            "price": [""],
            "country_dep": [""],
            "country_arr": [""],
            "date_dep": [""],
            "date_arr": [""],
            "provider_name": [""],
            "id_vol": [""],
            "date_book": [""],
            "flight_number": [""],
        }

    if books:
        for flight, procure, classe, price, provider in result:
            l["price"].append(price.price_value)
            l["country_dep"].append(flight.country_dep)
            l["country_arr"].append(flight.country_arr)
            l["date_dep"].append(str(flight.date_dep))
            l["date_arr"].append(str(flight.date_arr))
            l["provider_name"].append(provider.name_provider)
            l["id_vol"].append(flight.id_flight)
            l["capacity_left"].append(
                    flightHasCapacityLeft(int(flight.id_flight),
                                          int(procure.id_class)))
    else:
        for flight, procure, classe, price, provider, book in result:
            l["price"].append(price.price_value)
            l["country_dep"].append(flight.country_dep)
            l["country_arr"].append(flight.country_arr)
            l["date_dep"].append(str(flight.date_dep))
            l["date_arr"].append(str(flight.date_arr))
            l["provider_name"].append(provider.name_provider)
            l["id_vol"].append(flight.id_flight)
            l["date_book"].append(str(book.date_book))
            l["flight_number"].append(book.flight_number)

    # print(l)

    return l


def flightHasCapacityLeft(idflight: int, classe: int) -> bool:
    # Vérification de la relation flight-provider-class

    procure = session.query(Procure).filter(
        Procure.id_flight == idflight,
        Procure.id_provider == Provider.id_provider,
        Procure.class_.has(id_class=classe)
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
        return False

    return True

# getResultsFrom(searchFlight(provider_name="Air France"))
# getResultsFrom(searchFlight(price=350, cmp="supequals"))
