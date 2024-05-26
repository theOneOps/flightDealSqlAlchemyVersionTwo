from creation_table import *
from utils import *

session = Session()

# insertions of Users 'records
for user_data in users_data:
    user = Users(**user_data)
    session.add(user)
session.commit()

# insertions of Flight 'records
for flight_data in flights_data:
    flight = Flight(**flight_data)
    session.add(flight)
session.commit()


# insertions of Price 'records
for price_data in prices_data:
    price = Price(**price_data)
    session.add(price)
session.commit()


# insertions of Provider 'records
for provider_data in providers_data:
    provider = Provider(**provider_data)
    session.add(provider)
session.commit()

# insertions of Class 'records
for class_data in classes_data:
    class_ = Classe(**class_data)
    session.add(class_)
session.commit()

# insertions of Class 'records
for procure_data in procures_data:
    procure = Procure(**procure_data)
    session.add(procure)
session.commit()

# insertions of Book 'records
for book_data in books_data:
    book = Book(**book_data)
    session.add(book)
session.commit()

session.close()










