import mysql.connector
class SqlAccess:
    def __init__(self):

        # inserts rows into TechCrunchcontinentalUSA table
        @staticmethod
        def insert_record(obj_list):
            cnx = mysql.connector.connect(user='user1', password='password123',
                                          host='127.0.0.1', database='records',
                                          auth_plugin='mysql_native_password')
            cursor = cnx.cursor()
            add_record = ("INSERT INTO TechCrunchcontinentalUSA"
                          "(permalink, company, num_empls, category, city, state, funded_date, raised_amount, raised_currency, round)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            for obj in list:
                if obj.numEmps == '':
                    obj.numEmps = None
                date_obj = parse(obj.fundedDate)
                data_record = (obj.permalink, obj.company, obj.numEmps, obj.category, obj.city,
                               obj.state, date_obj, obj.raisedAmt, obj.raisedCurrency, obj.round)
                cursor.execute(add_record, data_record)

            cnx.commit()
            cursor.close()
            cnx.close()
