from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("mysql+mysqlconnector://root:@localhost"
                       "/flightdealnewversion",
                       echo=None)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    books = relationship("Book", back_populates="user")


class Flight(Base):
    __tablename__ = 'flight'
    id_flight = Column(Integer, primary_key=True, autoincrement=True)
    date_dep = Column(Date)
    date_arr = Column(Date)
    country_dep = Column(String(50))
    country_arr = Column(String(50))
    books = relationship("Book", back_populates="flight")
    procures = relationship("Procure", back_populates="flight")


class Provider(Base):
    __tablename__ = 'provider'
    id_provider = Column(Integer, primary_key=True, autoincrement=True)
    name_provider = Column(String(50), nullable=False)
    procures = relationship("Procure", back_populates="provider")


class Classe(Base):
    __tablename__ = 'classe'
    id_class = Column(Integer, primary_key=True, autoincrement=True)
    capacity = Column(Integer)
    name_class = Column(String(50))
    books = relationship("Book", back_populates="class_")
    procures = relationship("Procure", back_populates="class_")


class Price(Base):
    __tablename__ = 'price'
    id_price = Column(Integer, primary_key=True, autoincrement=True)
    price_value = Column(Float)
    books = relationship("Book", back_populates="price")
    procures = relationship("Procure", back_populates="price")


class Book(Base):
    __tablename__ = 'book'
    id_book = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(Integer)
    date_book = Column(Date)
    id_price = Column(Integer, ForeignKey('price.id_price'))
    id_class = Column(Integer, ForeignKey('classe.id_class'))
    id_flight = Column(Integer, ForeignKey('flight.id_flight'))
    id_user = Column(Integer, ForeignKey('users.id_user'))

    price = relationship("Price", back_populates="books")
    class_ = relationship("Classe", back_populates="books")
    flight = relationship("Flight", back_populates="books")
    user = relationship("Users", back_populates="books")


class Procure(Base):
    __tablename__ = 'procure'
    id_flight = Column(Integer, ForeignKey('flight.id_flight'),
                       primary_key=True)
    id_provider = Column(Integer, ForeignKey('provider.id_provider'),
                         primary_key=True)
    id_class = Column(Integer, ForeignKey('classe.id_class'), primary_key=True)
    id_price = Column(Integer, ForeignKey('price.id_price'), primary_key=True)

    flight = relationship("Flight", back_populates="procures")
    provider = relationship("Provider", back_populates="procures")
    class_ = relationship("Classe", back_populates="procures")
    price = relationship("Price", back_populates="procures")


# Configuration de la connexion à la base de données (à adapter selon votre cas)
Base.metadata.create_all(engine)

# Création et utilisation d'une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()
session.commit()
session.close()
