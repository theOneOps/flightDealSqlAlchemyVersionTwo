from datetime import date

# users's table data
users_data = [
    {"name": "AliceMartin", "email": "alice.martin@example.com",
     "password": "password123"},
    {"name": "BobSmith", "email": "bob.smith@example.com",
     "password": "safePassword321"},
    {"name": "CharlieBrown", "email": "charlie.brown@example.com",
     "password": "mySecurePass456"},
    {"name": "DavidWilson", "email": "david.wilson@example.com",
     "password": "pass789Secure"},
    {"name": "EvaGreen", "email": "eva.green@example.com",
     "password": "greenPass234"},
    {"name": "FionaClark", "email": "fiona.clark@example.com",
     "password": "clarkPass987"},
    {"name": "GeorgeHall", "email": "george.hall@example.com",
     "password": "hallPass654"},
    {"name": "HelenAllen", "email": "helen.allen@example.com",
     "password": "allen123Password"},
    {"name": "IvanMorris", "email": "ivan.morris@example.com",
     "password": "morris321Pass"},
    {"name": "JuliaHarris", "email": "julia.harris@example.com",
     "password": "juliaSecure456"}
]

# provider's table data
providers_data = [
    {"name_provider": "Air France"},
    {"name_provider": "Lufthansa"},
    {"name_provider": "British Airways"},
    {"name_provider": "Emirates"},
    {"name_provider": "Delta Airlines"},
    {"name_provider": "American Airlines"},
    {"name_provider": "Qatar Airways"},
    {"name_provider": "Singapore Airlines"},
    {"name_provider": "Cathay Pacific"},
    {"name_provider": "KLM"}
]

# flight's table data

flights_data = [
    {"date_dep": date(2024, 6, 1), "date_arr": date(2024, 6, 1),
     "country_dep": "France", "country_arr": "Germany"},
    {"date_dep": date(2024, 6, 2), "date_arr": date(2024, 6, 2),
     "country_dep": "United Kingdom", "country_arr": "United States"},
    {"date_dep": date(2024, 6, 3), "date_arr": date(2024, 6, 3),
     "country_dep": "United Arab Emirates", "country_arr": "Australia"},
    {"date_dep": date(2024, 6, 4), "date_arr": date(2024, 6, 4),
     "country_dep": "United States", "country_arr": "Japan"},
    {"date_dep": date(2024, 6, 5), "date_arr": date(2024, 6, 5),
     "country_dep": "Qatar", "country_arr": "Singapore"},
    {"date_dep": date(2024, 6, 6), "date_arr": date(2024, 6, 6),
     "country_dep": "Netherlands", "country_arr": "China"},
    {"date_dep": date(2024, 6, 7), "date_arr": date(2024, 6, 7),
     "country_dep": "Hong Kong", "country_arr": "Canada"},
    {"date_dep": date(2024, 6, 8), "date_arr": date(2024, 6, 8),
     "country_dep": "Germany", "country_arr": "Brazil"},
    {"date_dep": date(2024, 6, 9), "date_arr": date(2024, 6, 9),
     "country_dep": "United Kingdom", "country_arr": "India"},
    {"date_dep": date(2024, 6, 10), "date_arr": date(2024, 6, 10),
     "country_dep": "France", "country_arr": "South Africa"}
]

# price's table data

prices_data = [
    {"price_value": 200.0},
    {"price_value": 350.0},
    {"price_value": 450.0},
    {"price_value": 600.0},
    {"price_value": 750.0},
    {"price_value": 900.0},
    {"price_value": 1200.0},
    {"price_value": 1500.0},
    {"price_value": 1800.0},
    {"price_value": 2200.0}
]

# class's table data

classes_names = ["", "Economy", "Premium Economy", "Business", "First Class"]

classes_data = [
    {"capacity": 50, "name_class": "Economy"},
    {"capacity": 30, "name_class": "Premium Economy"},
    {"capacity": 20, "name_class": "Business"},
    {"capacity": 10, "name_class": "First Class"}
]

# procure's table data

procures_data = [
    {"id_flight": 1, "id_provider": 1, "id_class": 1, "id_price": 1},
    {"id_flight": 2, "id_provider": 2, "id_class": 2, "id_price": 2},
    {"id_flight": 3, "id_provider": 3, "id_class": 3, "id_price": 3},
    {"id_flight": 4, "id_provider": 4, "id_class": 4, "id_price": 4},
    {"id_flight": 5, "id_provider": 5, "id_class": 1, "id_price": 5},
    {"id_flight": 6, "id_provider": 6, "id_class": 2, "id_price": 6},
    {"id_flight": 7, "id_provider": 7, "id_class": 3, "id_price": 7},
    {"id_flight": 8, "id_provider": 8, "id_class": 4, "id_price": 8},
    {"id_flight": 9, "id_provider": 9, "id_class": 1, "id_price": 9},
    {"id_flight": 10, "id_provider": 10, "id_class": 2, "id_price": 10}
]

# book's table data
books_data = [
    {"flight_number": 1001, "date_book": date(2024, 5, 20), "id_price": 1,
     "id_class": 1, "id_flight": 1, "id_user": 1},
    {"flight_number": 1002, "date_book": date(2024, 5, 21), "id_price": 2,
     "id_class": 2, "id_flight": 2, "id_user": 2},
    {"flight_number": 1003, "date_book": date(2024, 5, 22), "id_price": 3,
     "id_class": 3, "id_flight": 3, "id_user": 3},
    {"flight_number": 1004, "date_book": date(2024, 5, 23), "id_price": 4,
     "id_class": 4, "id_flight": 4, "id_user": 4},
    {"flight_number": 1005, "date_book": date(2024, 5, 24), "id_price": 5,
     "id_class": 1, "id_flight": 5, "id_user": 5},
    {"flight_number": 1006, "date_book": date(2024, 5, 25), "id_price": 6,
     "id_class": 2, "id_flight": 6, "id_user": 6},
    {"flight_number": 1007, "date_book": date(2024, 5, 26), "id_price": 7,
     "id_class": 3, "id_flight": 7, "id_user": 7}
]


def center_window(root, width: int, height: int, offset_y: int = 55):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position x and y coordinates
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) - offset_y

    root.geometry(f"{width}x{height}+{x}+{y}")
