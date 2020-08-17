import mysql.connector
import csv
import table_setup as Setup
import models.CompanyRecord as CompanyRecord
import models.Sales as Sales
import models.RealEstateTransaction as Transaction
import os
from dateutil.parser import parse
from mysql.connector import errorcode


class SqlAccess:
    def __init__(self):
        self._user = 'user1'
        self._password = 'password123'
        self._host = '127.0.0.1'
        self._db_name = 'records'
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.createConnection()

    def create_tables_and_insert(self):
        cursor = self._cnx.cursor()
        tables = Setup.DataSetup().get_table_creation()

        # if table does not exist, create it, parse csv, then insert into table
        # if table exists, assume the csv has already been parsed and continue
        for table_name in tables:
            table_description = tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
                csv_path = self.root_dir + '/data/' + table_name + '.csv'
                reader = list(csv.reader(open(csv_path)))
                data_objects = []
                # get list of objects for table_name
                if table_name == 'TechCrunchcontinentalUSA':
                    for row in reader:
                        data_objects.append(CompanyRecord.Record(*row[0:]))
                    del data_objects[0]
                    self.insert_record(data_objects)
                elif table_name == 'SalesJan2009':
                    for row in reader:
                        data_objects.append(Sales.Sales(*row[0:]))
                    del data_objects[0]
                    self.insert_sale(data_objects)
                elif table_name == 'Sacramentorealestatetransactions':
                    for row in reader:
                        data_objects.append(Transaction.RealEstateTransaction(*row[0:]))
                    del data_objects[0]
                    self.insert_transaction(data_objects)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Table already exists. Exiting...")
                else:
                    print(err.msg)
            else:
                print("Table successfully created.")
        cursor.close()
        self._cnx.close()

    # inserts rows into TechCrunchcontinentalUSA table
    def insert_record(self, obj_list):
        cursor = self._cnx.cursor()
        add_record = ("INSERT INTO TechCrunchcontinentalUSA" 
                      "(permalink, company, num_empls, category, city, state,"
                      " funded_date, raised_amount, raised_currency, round)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        for obj in obj_list:
            if obj.numEmps == '':
                obj.numEmps = None
            date_obj = parse(obj.fundedDate)
            data_record = (obj.permalink, obj.company, obj.numEmps, obj.category, obj.city,
                           obj.state, date_obj, obj.raisedAmt, obj.raisedCurrency, obj.round)
            cursor.execute(add_record, data_record)

        self._cnx.commit()
        cursor.close()

    def insert_sale(self, obj_list):
        cursor = self._cnx.cursor()
        add_record = ("INSERT INTO SalesJan2009"
                      "(transaction_date, product, price, payment_type, name, "
                      "city, state, country, account_created, last_login, latitude, longitude)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        for obj in obj_list:
            obj.tDate = parse(obj.tDate)
            obj.accountCreated = parse(obj.accountCreated)
            obj.lastLogin = parse(obj.lastLogin)
            data_record = (obj.tDate, obj.product, obj.price, obj.paymentType,
                           obj.name, obj.city, obj.state, obj.country, obj.accountCreated,
                           obj.lastLogin, obj.latitude, obj.longitude)
            cursor.execute(add_record, data_record)

        self._cnx.commit()
        cursor.close()

    def insert_transaction(self, obj_list):
        cursor = self._cnx.cursor()
        add_record = ("INSERT INTO Sacrementorealestatetransactions"
                      "(street, city, state, zip, state, beds, baths, sq_feet"
                      "type, sale_date, price, latitude, longitude)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        for obj in obj_list:
            obj.saleDate = parse(obj.saleDate)
            data_record = (obj.tDate, obj.product, obj.price, obj.paymentType,
                           obj.name, obj.city, obj.state, obj.country, obj.accountCreated,
                           obj.accountCreated, obj.lastLogin, obj.latitude, obj.longitude)
            cursor.execute(add_record, data_record)

        self._cnx.commit()
        cursor.close()

    def createConnection(self):
        cnx = mysql.connector.connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._db_name,
            auth_plugin='mysql_native_password')
        self._cnx = cnx
