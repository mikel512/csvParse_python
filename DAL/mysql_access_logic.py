import mysql.connector
import csv
from DAL import table_setup as Setup
import models.CompanyRecord as CompanyRecord
import models.Sales as Sales
import models.RealEstateTransaction as Transaction
import models.CrimeRecord as CrimeRecord
import models.SbaData as sba
import os
import sys
from dateutil.parser import parse
from mysql.connector import errorcode


class SqlAccess:
    def __init__(self):
        self._user = 'user1'
        self._password = 'password123'
        self._host = '127.0.0.1'
        self._db_name = 'records'
        self.root_dir = os.path.dirname(sys.modules['__main__'].__file__)
        self.createConnection()

    def create_tables_and_insert(self):
        cursor = self._cnx.cursor()
        tables = Setup.DataSetup().get_table_creation()
        drop_tables = ("DROP TABLE if exists `sacramentocrimejanuary2006`, `salesjan2009`, `techcrunchcontinentalusa`, "
                       "`sacramentorealestatetransactions`; ")
        cursor.execute(drop_tables)

        # if table does not exist, create it, parse csv, then insert into table
        # if table exists, assume the csv has already been parsed and continue
        for table_name in tables:
            table_description = tables[table_name]
            try:
                print("Creating table {}: ".format(table_name))
                cursor.execute(table_description)
                csv_path = self.root_dir + '/data/' + table_name + '.csv'
                reader = list(csv.reader(open(csv_path)))
                data_objects = []
                # get list of objects for table_name
                print('Inserting rows into {}'.format(table_name))
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
                elif table_name == 'SacramentocrimeJanuary2006':
                    for row in reader:
                        data_objects.append(CrimeRecord.CrimeRecord(*row[0:]))
                    del data_objects[0]
                    self.insert_crimerec(data_objects)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Table already exists. Exiting...")
                else:
                    print(err.msg)
            else:
                print("Table successfully created.")
        cursor.close()
        self._cnx.close()

    def create_sbaentry_tables(self):
        cursor = self._cnx.cursor()
        tables = Setup.DataSetup().get_sba_table_creation()
        drop_tables = ("DROP TABLE if exists `entry_theme`, `keyword_entry`, `entry_distribution`, "
                       "`distribution`, `theme`, `keyword`, `sba_entry`, "
                       "`contact_point`, `publisher`; ")
        cursor.execute(drop_tables)
        for table_name in tables:
            table_description = tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Table already exists. Exiting...")
                else:
                    print(err.msg)
            else:
                print("Tables successfully created.")

    # inserts sba entries from a list of objects
    # it maintains a dictionary of the primary keys of entries that
    # might be seen again in order to avoid inserting duplicates.
    def insert_sba_entries(self, data_list):
        seen_dict = {}
        seen_keywords = {}
        seen_distros = {}
        cursor = self._cnx.cursor()
        objs_inserted = 0
        print('Beginning insertion to database...')

        for entry in data_list:
            objs_inserted += 1
            # foreign keys to be entered at the end
            f_keys = {}
            if entry.publisher is not None:
                if seen_dict.get(entry.publisher.name) is not None:
                    f_keys['publisher'] = seen_dict[entry.publisher.name]
                else:
                    add_record = ("INSERT INTO publisher "
                                  "(name) "
                                  "VALUES (%s)")
                    data_record = (entry.publisher.name,)
                    cursor.execute(add_record, data_record)
                    # add primary key to dictionary
                    seen_dict[entry.publisher.name] = cursor.lastrowid
                    f_keys['publisher'] = seen_dict[entry.publisher.name]

            if entry.contactPoint is not None:
                if seen_dict.get(entry.contactPoint.fn) is not None:
                    f_keys['contact'] = seen_dict[entry.contactPoint.fn]
                else:
                    add_record = ("INSERT INTO contact_point"
                                  "(fn, has_email) "
                                  "VALUES (%s, %s)")
                    data_record = (entry.contactPoint.fn, entry.contactPoint.email)
                    cursor.execute(add_record, data_record)
                    seen_dict[entry.contactPoint.fn] = cursor.lastrowid
                    f_keys['contact'] = seen_dict[entry.contactPoint.fn]

            # f_keys['distros'] is a list of distribution id's
            if entry.distributions is not None:
                f_keys['distros'] = []
                for distro in entry.distributions:
                    # check if distro is accessURL or downloadURL
                    if distro.accessUrl is not None:
                        if seen_distros.get(distro.accessUrl) is not None:
                            f_keys['distros'].append(seen_distros[distro.accessUrl])
                        else:
                            add_record = ("INSERT INTO distribution"
                                          "(media_type, title, description, download_url, access_url) "
                                          "VALUES (%s, %s, %s, %s, %s)")
                            data_record = (distro.mediaType, distro.title, distro.description,
                                           distro.downloadUrl, distro.accessUrl)
                            cursor.execute(add_record, data_record)
                            seen_distros[distro.accessUrl] = cursor.lastrowid
                            f_keys['distros'].append(seen_distros[distro.accessUrl])
                    # if its a downloadURL
                    else:
                        if seen_distros.get(distro.downloadUrl) is not None:
                            f_keys['distros'].append(seen_distros[distro.downloadUrl])
                        else:
                            add_record = ("INSERT INTO distribution"
                                          "(media_type, title, description, download_url, access_url) "
                                          "VALUES (%s, %s, %s, %s, %s)")
                            data_record = (distro.mediaType, distro.title, distro.description,
                                           distro.downloadUrl, distro.accessUrl)
                            cursor.execute(add_record, data_record)
                            seen_distros[distro.downloadUrl] = cursor.lastrowid
                            f_keys['distros'].append(seen_distros[distro.downloadUrl])

            # f_keys['keywords'] is a list of keyword id's
            if entry.keywords is not None:
                f_keys['keywords'] = []
                for kw in entry.keywords:
                    if seen_keywords.get(kw) is not None:
                        f_keys['keywords'].append(seen_keywords[kw])
                    else:
                        add_record = ("insert into keyword"
                                      "(name) "
                                      "values (%s)")
                        data_record = (kw,)
                        cursor.execute(add_record, data_record)
                        seen_keywords[kw] = cursor.lastrowid
                        f_keys['keywords'].append(seen_keywords[kw])

            # f_keys['themes'] is a list of theme id's
            if entry.theme is not None:
                f_keys['themes'] = []
                for th in entry.theme:
                    if seen_dict.get(th) is not None:
                        f_keys['themes'].append(seen_dict[th])
                    else:
                        add_record = ("insert into theme"
                                      "(name) "
                                      "values (%s)")
                        data_record = (th,)
                        cursor.execute(add_record, data_record)
                        seen_dict[th] = cursor.lastrowid
                        f_keys['themes'].append(seen_dict[th])

            add_record = ("INSERT INTO sba_entry"
                          "(title, description, modified, access_level, identifier, issued,"
                          "landing_page, license, publisher_no, accrual_periodicity, is_part_of,"
                          "contact_no, bureau_code, program_code) "
                          "VALUES (%s, %s, %s, %s, %s, %s,"
                          "%s, %s, %s, %s, %s,"
                          "%s, %s, %s )")
            if entry.modified is not None:
                entry.modified = parse(entry.modified)
            if entry.issued is not None:
                entry.issued = parse(entry.issued)
            data_record = (entry.title, entry.description, entry.modified, entry.accessLevel,
                           entry.identifier, entry.issued, entry.landingPage, entry.license,
                           f_keys['publisher'], entry.accrualPeriodicity, entry.isPartOf,
                           f_keys['contact'], entry.bureauCode, entry.programCode)
            cursor.execute(add_record, data_record)
            entry_id = cursor.lastrowid

            # insert many to many relationships
            for distr in f_keys['distros']:
                add_record = ("insert into entry_distribution"
                              "(dist_no, entry_no) "
                              "values (%s, %s)")
                data_record = (distr, entry_id)
                cursor.execute(add_record, data_record)

            for kw in f_keys['keywords']:
                add_record = ("insert into keyword_entry"
                              "(kw_no, entry_no) "
                              "values (%s, %s)")
                data_record = (kw, entry_id)
                cursor.execute(add_record, data_record)

            if entry.theme is not None:
                for theme in f_keys['themes']:
                    add_record = ("insert into entry_theme"
                                  "(theme_no, entry_no) "
                                  "values (%s, %s)")
                    data_record = (theme, entry_id)
                    cursor.execute(add_record, data_record)

            self._cnx.commit()
            f_keys.clear()
        print('{} objects inserted to database'.format(objs_inserted))


    # inserts rows into techcrunchcontinentalusa table
    def insert_record(self, obj_list):
        cursor = self._cnx.cursor()
        add_record = ("insert into techcrunchcontinentalusa" 
                      "(permalink, company, num_empls, category, city, state,"
                      " funded_date, raised_amount, raised_currency, round)"
                      "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
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
        add_record = ("INSERT INTO Sacramentorealestatetransactions"
                      "(street, city, state, zip, beds, baths, sq_feet,"
                      "type, sale_date, price, latitude, longitude)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        for obj in obj_list:
            obj.saleDate = parse(obj.saleDate)
            data_record = (obj.street, obj.city, obj.state, obj.zip, obj.beds,
                           obj.baths, obj.squareFeet, obj.type, obj.saleDate,
                           obj.price, obj.latitude, obj.longitude)
            cursor.execute(add_record, data_record)

        self._cnx.commit()
        cursor.close()

    def insert_crimerec(self, obj_list):
        cursor = self._cnx.cursor()
        add_record = ("INSERT INTO SacramentocrimeJanuary2006"
                      "(crime_date, address, district, beat, grid, crime_description,"
                      "ucr_ncic_code, latitude, longitude)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        for obj in obj_list:
            obj.crimeDate = parse(obj.crimeDate)
            data_record = (obj.crimeDate, obj.address, obj.district, obj.beat, obj.grid,
                           obj.crimeDescription, obj.code, obj.latitude, obj.longitude)
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
