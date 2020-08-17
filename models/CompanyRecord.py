import csv
import mysql.connector
import dateutil.parser


class Record:
    def __init__(self, permalink, company, numEmps, category,
            city, state, fundedDate, raisedAmt, raisedCurrency, round):
        self.permalink = permalink
        self.company = company
        self.numEmps = numEmps
        self.category = category
        self.city = city
        self.state = state
        self.fundedDate = fundedDate
        self.raisedAmt = raisedAmt
        self.raisedCurrency = raisedCurrency
        self.round = round
