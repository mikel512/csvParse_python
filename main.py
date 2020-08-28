import sql_access_logic as logic
import models.SbaData as data

if __name__ == '__main__':
    sba_data = data.SbaData()
    data_list = sba_data.ParseJsonData()
    execute = logic.SqlAccess()
    execute.create_sbaentry_tables()

    pass
    #execute.create_tables_and_insert()
