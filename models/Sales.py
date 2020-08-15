import csv

class Sales:
    def __init__(self, t_date, product, price, payment_type,
                 name, city, state, country, account_created, last_login, latitude, longitude):
        self.tDate = t_date
        self.product = product
        self.price = price
        self.paymentType = payment_type
        self.name = name
        self.city = city
        self.state = state
        self.country = country
        self.accountCreated = account_created
        self.lastLogin = last_login
        self.latitude = latitude
        self.longitude = longitude

