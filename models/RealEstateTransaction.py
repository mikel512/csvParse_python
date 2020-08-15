class RealEstateTransaction:
    def __init__(self, street, city, zip, state, beds, baths, sq_ft,
                 type, sale_date, price, latitude, longitude):
        self.street = street
        self.city = city
        self.zip = zip
        self.state = state
        self.beds = beds
        self.baths = baths
        self.squareFeet = sq_ft
        self.type = type
        self.saleDate = sale_date
        self.price = price
        self.latitude = latitude
        self.longitude = longitude