import \
    datetime  # Import the datetime module to handle date and time operations.
import math  # Import the math module for mathematical operations.
from typing import \
    Any  # Import Any from typing to support variable annotations.

from sqlalchemy import \
    and_  # Import 'and_' for constructing SQL AND conditions in queries.
from sqlalchemy.exc import \
    NoResultFound  # Import exception to handle queries that return no result.

from model.creation_table import *  # Import all from creation_table to access database table definitions.

# Define a type alias for better clarity and type hinting for user information.
type userType = {"id": int, "name": str, "passwd": str}

# Initialize a variable to keep track of the currently connected user.
userConnect: userType = {"id": None, "name": "", "passwd": ""}

# Create a session object from sessionmaker to handle transactions with the database.
Session = sessionmaker(bind=engine)
session = Session()


# Define a function to add a user to the database.
def addUser(name: str, passwd: str, email: str = "") -> bool:
    try:
        # Attempt to retrieve a user with the provided name.
        result = session.query(Users).filter(Users.name == name).one()
        print("user already existed ! ")
        # If a user exists, return False indicating user creation was not successful.
        return False
    except NoResultFound:
        # If no user exists with the provided name, create a new user.
        new_user = Users(name=name, password=passwd, email=email)
        session.add(new_user)  # Add the new user to the session.
        session.commit()  # Commit the transaction to save the user to the database.
        print("user created successfully ! ")
        # Return True indicating the user was successfully created.
        return True


# Define a function to authenticate and connect a user.
def connectUser(name: str, passwd: str, email: str = "") -> bool:
    global userConnect  # Use the global userConnect to update the currently connected user.
    try:
        # Attempt to retrieve a user matching both the provided name and password.
        result = session.query(Users).filter(and_(Users.name == name,
                                                  Users.password == passwd)).one()
        if result:
            # If such a user is found, update userConnect with the user's details.
            userConnect["id"] = result.id_user
            userConnect["name"] = result.name
            userConnect["passwd"] = result.password
            print(f"user {name} logged in successfully !")
            # Return True indicating successful login.
            return True
    except NoResultFound:
        # If no matching user is found, print an error message and return False.
        print(f'there is no account for username {name} and password {passwd}')
        return False


# Define a function to check if a user is currently connected.
def isUserConnected() -> bool:
    global userConnect  # Access the global variable to check the current user's connection status.
    if userConnect["id"] is not None:
        # If the 'id' of the userConnect is not None, the user is considered connected.
        return True
    # If 'id' is None, no user is currently connected.
    return False


# Define a function to disconnect the current user.
def disconnectUser() -> bool:
    global userConnect  # Access the global variable to update the current user's connection status.
    if userConnect["id"] is not None:
        # If a user is connected (i.e., 'id' is not None):
        userConnect[
            "id"] = None  # Set the 'id' to None to indicate no user is connected.
        userConnect["name"] = ""  # Clear the 'name' field.
        userConnect["passwd"] = ""  # Clear the 'passwd' field.
        print(
            f"user logged out successfully !")  # Print a logout success message.
        return True  # Return True indicating the user was successfully logged out.
    # If no user was connected to start with, return False.
    return False


# disconnectUser()

# Define a function to search for flights based on multiple filter criteria.
def searchFlight(type_seat: str = "", date_dep: str = "", date_arr: str = "",
                 country_dep: str = "", country_arr: str = "",
                 price: float = math.inf,
                 cmp: str = "equals", provider_name: str = "") -> Any:
    # Setup the initial query joining several tables related to flights.
    result = session.query(Flight, Procure, Classe, Price, Provider).join(
        Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                            Procure.id_class ==
                                                            Classe.id_class).join(
        Price, Price.id_price == Procure.id_price).join(Provider,
                                                        Provider.id_provider == Procure.id_provider)

    # Apply filters based on function arguments if they are not empty or their default values.
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

    # Apply price filter based on the comparison type.
    if price != math.inf:
        price_filters = {
            "equals": Price.price_value == price,
            "inf": Price.price_value < price,
            "infequals": Price.price_value <= price,
            "supequals": Price.price_value >= price,
            "sup": Price.price_value > price
        }
        result = result.filter(price_filters.get(cmp,
                                                 None))  # Use dictionary to simplify the logic.

    # If no specific filters are applied, fetch all records.
    if not any(
            [country_dep, country_arr, type_seat, price != math.inf, date_dep,
             date_arr, provider_name]):
        result = session.query(Flight, Procure, Classe, Price, Provider).join(
            Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                                Procure.id_class ==
                                                                Classe.id_class).join(
            Price, Price.id_price == Procure.id_price).join(Provider,
                                                            Provider.id_provider == Procure.id_provider).all()
    else:
        result = result.all()

    # Print the result in a formatted way if any records are found.
    # if result:
    #     line_format = (
    #         "| {:<18} | {:<20} | {:<20} | {:<18} | {:<20} | {:<20} | {}")
    #     print(line_format.format("name_provider", "country_dep", "country_arr",
    #                              "date_dep", "date_arr", "classe", "price"))
    #     for flight, procure, classe, price, provider in result:
    #         print(line_format.format(provider.name_provider,
    #                                  flight.country_dep, flight.country_arr,
    #                                  str(flight.date_dep), str(flight.date_arr),
    #                                  classe.name_class, price.price_value))
    # else:
    #     print("there is no records found for your request !")

    return result  # Return the search result, which can be further processed or displayed.


# searchFlight()
# searchFlight(provider_name="Air France")

# Define a function to book a flight, requiring class type, flight ID, and provider name.
def bookFlight(classe: str, idflight: int, providername: str) -> str:
    global userconnect  # Access the global variable for user connection details.

    # Check if the user is logged in.
    if userConnect["id"] is None:
        print("You need login to proceed")
        return "You need login to proceed"

    try:
        # Query the database for the specified flight using the provided flight ID.
        flight = session.query(Flight).filter(
            Flight.id_flight == idflight).first()
        # If the flight does not exist, return a message indicating so.
        if not flight:
            return "Le vol n'existe pas."

        # Query the database for the provider using the provided provider name.
        provider = session.query(Provider).filter(
            Provider.name_provider == providername).first()
        # If the provider does not exist, return a message indicating so.
        if not provider:
            return "Le fournisseur n'existe pas."

        # Check if there is a valid procurement entry linking the flight, provider, and class.
        procure = session.query(Procure).filter(
            Procure.id_flight == idflight,
            Procure.id_provider == provider.id_provider,
            Procure.class_.has(name_class=classe)
        ).first()
        # If no such procurement entry exists, return an error message.
        if not procure:
            return "Le fournisseur ne propose pas cette classe pour ce vol."

        # Verify the availability of seats in the specified class.
        class_capacity = procure.class_.capacity
        current_bookings = session.query(Book).filter(
            Book.id_flight == idflight,
            Book.id_class == procure.class_.id_class
        ).count()
        # If the number of current bookings meets or exceeds capacity, return a no seat available message.
        if current_bookings >= class_capacity:
            return f"Pas de sièges disponibles en classe {classe}."

        # Create a new booking entry.
        new_booking = Book(
            flight_number=current_bookings + 1,
            # Increment the flight number for this booking.
            date_book=datetime.date.today(),  # Set the booking date to today.
            id_price=procure.id_price,
            # Set the price ID from the procurement entry.
            id_class=procure.id_class,
            # Set the class ID from the procurement entry.
            id_flight=idflight,  # Set the flight ID from the input.
            id_user=userConnect["id"]
            # Set the user ID from the currently logged-in user.
        )

        # Add the new booking to the session and commit it to the database.
        session.add(new_booking)
        session.commit()
        # Print and return a successful booking message.
        print(
            f"Réservation réussie en classe {classe} pour le vol {idflight} avec {providername}.")
        return f"Réservation réussie en classe {classe} pour le vol {idflight} avec {providername}."
    except NoResultFound:
        # Handle cases where no results were found in the query.
        return "Erreur lors de la réservation : données introuvables."
    except Exception as e:
        # Rollback the session in case of any other exceptions and print an error message.
        session.rollback()
        print(f"Erreur lors de la réservation : {str(e)}")
        return f"Erreur lors de la réservation : {str(e)}"


# Define a function to search for booked flights based on multiple criteria.
def searchBook(type_seat: str = "", date_dep: str = "", date_arr: str = "",
               date_book: str = "", country_dep: str = "",
               country_arr: str = "",
               price: float = math.inf, cmp: str = "equals",
               provider_name: str = ""):
    global userConnect  # Access the global userConnect to check if a user is logged in.

    # Ensure the user is logged in before proceeding.
    if userConnect["id"] is not None:

        # Begin a query joining several tables related to flight booking details.
        result = (
            session.query(Flight, Procure, Classe, Price, Provider, Book).join(
                Flight, Flight.id_flight == Procure.id_flight).join(Classe,
                                                                    Procure.id_class == Classe.id_class).join(
                Price, Price.id_price == Procure.id_price).join(Provider,
                                                                Provider.id_provider == Procure.id_provider)
            .join(Book, Book.id_flight == Flight.id_flight).filter(
                Book.id_user == userConnect[
                    "id"]))  # Filter bookings by the logged-in user's ID.

        # Apply additional filters based on the function arguments if they are provided.
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

        # Apply a price filter based on the comparison type provided.
        price_filters = {
            "equals": Price.price_value == price,
            "inf": Price.price_value < price,
            "infequals": Price.price_value <= price,
            "supequals": Price.price_value >= price,
            "sup": Price.price_value > price
        }
        if price != math.inf:
            result = result.filter(price_filters.get(cmp,
                                                     None))  # Use dictionary to simplify logic.

        # If no filters are provided, retrieve all bookings for the user.
        if not any([country_dep, country_arr, type_seat, price != math.inf,
                    date_dep, date_arr,
                    provider_name, date_book]):
            result = result.all()
        else:
            result = result.all()

        # Print the results in a formatted manner if any records are found.
        # if result:
        #     line_format = (
        #         "|{:<20} | {:<20} | {:<18} | {:<20} | {:<20} | {:<18} | {:<20} | {:<20} | {}")
        #     print(line_format.format("flight_number", "date of book",
        #                              "name_provider", "country_dep",
        #                              "country_arr", "date_dep", "date_arr",
        #                              "classe", "price"))
        #     for flight, procure, classe, price, provider, book in result:
        #         print(
        #             line_format.format(book.flight_number, str(book.date_book),
        #                                provider.name_provider,
        #                                flight.country_dep, flight.country_arr,
        #                                str(flight.date_dep),
        #                                str(flight.date_arr), classe.name_class,
        #                                price.price_value))
        # else:
        #     print("there is no records found for your request !")
        return result
    else:
        # Raise an exception if the user is not logged in.
        raise Exception("you should be connect first")


# addUser("johndoe", "azerty")
# connectUser("johndoe", "azerty")

# searchBook()


# bookFlight("Economy", 1, "Air France")

# def cancelBook(id_flight: int, id_book:int, class_name:str, provider_name:str)

## now the utility functions

# Define a function to transform database query results into a structured dictionary.
def getResultsFrom(result, books: bool = True) -> dict[str, list]:
    l: dict[
        str, list] = {}  # Initialize an empty dictionary to store the results.

    # Setup the dictionary structure based on whether the results are for booked flights or general flight info.
    if books:
        # Dictionary structure for booked flights.
        l = {
            "price": [""],
            "country_dep": [""],
            "country_arr": [""],
            "date_dep": [""],
            "date_arr": [""],
            "provider_name": [""],
            "id_vol": [""],
            "capacity_left": [],
            # Additional field for capacity left on the flight.
        }
    else:
        # Dictionary structure for general flight queries (non-booked specifics).
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

    # Populate the dictionary based on the results and the type of information requested.
    if books:
        # Iterate over each tuple in the result set for booked flights.
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
                                      int(procure.id_class)))  # Calculate remaining capacity.
    else:
        # Iterate over each tuple in the result set for general flight queries.
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

    # Optionally, the structure of 'l' can be printed for debugging purposes.
    # print(l)

    return l  # Return the populated dictionary.


# Define a function to check if there are available seats left on a flight for a specific class.
def flightHasCapacityLeft(idflight: int, classe: int) -> bool:
    # Query the Procure table to find the procurement details that link the flight ID and class ID.
    # This checks for the existence of a particular class available on a specific flight.
    procure = session.query(Procure).filter(
        Procure.id_flight == idflight,
        # Procure.id_provider == Provider.id_provider,
        # This line seems to contain an error since
        # Provider.id_provider is not contextualized.
        Procure.class_.has(id_class=classe)
        # Ensure the Procure record has the specific class ID.
    ).first()

    # If no procurement record is found, the provider may not offer
    # this class for the flight.
    if not procure:
        return "Le fournisseur ne propose pas cette classe pour ce vol."
        # This should be handled differently,
        # as the return type is bool.

    # Retrieve the capacity of the class from the procure record.
    class_capacity = procure.class_.capacity
    # Count how many bookings are already made for this specific flight and class.
    current_bookings = session.query(Book).filter(
        Book.id_flight == idflight,
        Book.id_class == procure.class_.id_class
    ).count()

    # Compare the number of current bookings to the class capacity.
    # If the number of bookings equals or exceeds the capacity, return False (no seats left).
    if current_bookings >= class_capacity:
        return False

    # If the number of current bookings is less than the capacity,
    # return True (seats available).
    return True


# getResultsFrom(searchFlight(provider_name="Air France"))
# getResultsFrom(searchFlight(price=350, cmp="supequals"))

def cancelBookingFlight(idbook: int):
    global userConnect
    if userConnect["id"] is None:
        return "You need login to proceed"

    book = session.query(Book).filter(Book.id_book == idbook).first()
    if not book:
        return f"Vous n'avez aucune une reservation sous cette id : {idbook}."

    # Check if the logged-in user is the one who made the booking.
    if book.id_user != userConnect["id"]:
        return "You do not have permission to cancel this booking."

    session.delete(book)
    session.commit()
    return f"Vous avez réussie à annuler votre reservation avec l'id :{idbook}"
