import models.CompanyRecord as CompanyRecord
import models.Sales as Sales
import models.RealEstateTransaction as RealEstateTransaction
import csv


# this class holds the methods to return lists of objects of the parsed csv files
class DataSetup:
    def __init__(self):
        self.tables = self.get_table_creation()

    # sets list of CompanyRecord objects
    @staticmethod
    def parse_transactions():
        result_list = []
        with open('Sacramentorealestatetransactions.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                result_list.append(RealEstateTransaction(row[0], row[1], row[2], row[3], row[4], row[5],
                                         row[6], row[7], row[8], row[9], row[10], row[11]))
        del result_list[0]
        return result_list

    # sets list of CompanyRecord objects
    @staticmethod
    def parse_records():
        result_list = []
        with open('TechCrunchcontinentalUSA.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                result_list.append(CompanyRecord(row[0], row[1], row[2], row[3],
                                          row[4], row[5], row[6], row[7], row[8], row[9]))
        del result_list[0]
        return result_list

    # returns list of Sales objects
    @staticmethod
    def parse_sales():
        result_list = []
        with open('SalesJan2009.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                result_list.append(Sales(row[0],row[1],row[2],row[3],row[4],row[5],
                                  row[6],row[7],row[8],row[9],row[10], row[11]))
        del result_list[0]
        return result_list

    # returns a dict of table creation scripts
    @staticmethod
    def get_table_creation():
        tables = {'TechCrunchcontinentalUSA': (
            "CREATE TABLE `TechCrunchcontinentalUSA` ("
            "  `rec_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `permalink` varchar(50) NOT NULL,"
            "  `company` varchar(50) NOT NULL,"
            "  `num_empls` int(11) ,"
            "  `category` varchar(30) NOT NULL,"
            "  `city` varchar(30) NOT NULL,"
            "  `state` varchar(30) NOT NULL,"
            "  `funded_date` date NOT NULL,"
            "  `raised_amount` int(11) ,"
            "  `raised_currency` varchar(30) NOT NULL,"
            "  `round` varchar(20) NOT NULL,"
            "  PRIMARY KEY (`rec_no`)"
            ") "),
            'SalesJan2009': (
            "CREATE TABLE `SalesJan2009` ("
            "  `sale_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `transaction_date` date NOT NULL,"
            "  `product` varchar(50) NOT NULL,"
            "  `price` int(11) ,"
            "  `payment_type` varchar(30) NOT NULL,"
            "  `name` varchar(30) NOT NULL,"
            "  `city` varchar(30) NOT NULL,"
            "  `state` varchar(30) NOT NULL,"
            "  `country` varchar(30) NOT NULL,"
            "  `account_created` date NOT NULL,"
            "  `last_login` date NOT NULL,"
            "  `latitude` int(11) ,"
            "  `longitude` int(11) ,"
            "  PRIMARY KEY (`sale_no`)"
            ") ")
        }
        return tables
