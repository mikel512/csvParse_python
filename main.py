import sql_access_logic as logic

if __name__ == '__main__':
    execute = logic.SqlAccess()
    execute.create_tables_and_insert()
