import models.SbaData as data
from DAL import couchdb_access as couchbase
from DAL import mongodb_access as mongodbaccess
from DAL import mysql_access_logic as sql_logic

if __name__ == '__main__':
    #sba data setup
    sba_data = data.SbaData()
    data_list = sba_data.ParseJsonData()

    # sql access
    execute = sql_logic.SqlAccess()
    execute.create_sbaentry_tables()
    execute.insert_sba_entries(data_list)
    execute.create_tables_and_insert()

    # mongoDB access
    mongo_access = mongodbaccess.MongoDbAccess()
    mongo_access.post_single_doc(sba_data.GetRawJson(), 0)

    # couchbase access
    couchdb = couchbase.CouchDbAccess()
    couchdb.upsert_doc(sba_data.GetRawJson(), '2000', 'sba')



