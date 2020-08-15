import models.CompanyRecord
import mysql.connector
from mysql.connector import errorcode
from dateutil.parser import parse




# creates tables if they dont already exist, then inserts rows
def createTables():
    cnx = mysql.connector.connect(user='user1', password='password123',
                            host='127.0.0.1', database='records',
                            auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    tables = getTableCreation()
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
            print("Table successfully created.")
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    parseList = parseCsv()
    createTables()
    insertFundingRecord(parseList)

