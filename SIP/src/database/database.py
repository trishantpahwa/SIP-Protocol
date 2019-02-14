from sqlite3 import connect
from sqlite3 import Error
from os.path import exists
import sys


class database:

    __tables = ['client_data', 'transfer_records']
    __client_data_column_types = [('id', 'int', 'PRIMARY KEY'),
                                  ('username', 'text', 'NOT NULL'),
                                  ('password', 'text', 'NOT NULL')]
    __transfer_records_column_types = [('id', 'int', 'PRIMARY KEY'),
                                       ('sender_name', 'text', 'NOT NULL'),
                                       ('receiver_name', 'text', 'NOT NULL'),
                                       ('sender_ip', 'text', 'NOT NULL'),
                                       ('receiver_ip', 'text', 'NOT NULL'),
                                       ('media_type', 'text', 'NOT NULL'),
                                       ('media_name', 'text', 'NOT NULL'),
                                       ('date', 'text', 'NOT NULL'),
                                       ('time', 'text', 'NOT NULL')]

    __client_data_columns = [x[0] for x in __client_data_column_types]
    __transfer_records_columns = [x[0] for x in __transfer_records_column_types]

    __table_name = None
    __columns = None
    __conn = None
    __c = None

    __statement = ''

    def __init__(self, table_name):
        db_file = 'C:\\Users\\r&dtrainee3\\Desktop\\SIP-Protocol\\SIP\\src\\database\\clients.db'  # Fix folder location
        self.__conn = connect(db_file)
        self.__c = self.__conn.cursor()
        if not exists(db_file):
            self.__create_database(db_file)
        self.__set_table_name(table_name)
        self.__set_columns()
        self.__conn = connect(db_file)
        self.__c = self.__conn.cursor()
        print('Connected to database')

    def __create_database(file_name):
        file = open(file_name, 'w')
        file.close()

    def __set_table_name(self, table_name):
        self.__statement = 'SELECT name from sqlite_master WHERE type=\"table\"'
        tables = self.__execute_query()
        if len(tables) > 0:
            for table in tables:
                if table_name in table[0]:
                    self.__table_name = table_name
        else:
            self.__table_name = table_name
            if table_name == 'client_data':
                self.__create_table(self.__client_data_column_types)
            if table_name == 'transfer_records':
                self.__create_table(self.__transfer_records_column_types)

    def __set_columns(self):
        if self.__table_name == 'client_data':
            self.__columns = self.__client_data_columns
        if self.__table__name == 'transfer_records':
            self.__columns = self.__transfer_records_columns

    def __execute_query(self):
        try:
            self.__c.execute(self.__statement)
            rows = self.__c.fetchall()
            return rows
        except Error:
            print(Error)

    def __disconnect_from_server(self):
        self.__conn.close()

    def print_records(self, columns=None):
        print_statement = 'SELECT '
        if columns is None:
            print_statement += '* FROM ' + self.__table_name
        else:
            for column in columns:
                print_statement += column + ','
            print_statement = print_statement.rstrip(', ') + ' FROM ' + \
                self.__table_name
        self.__statement = print_statement
        return self.__execute_query()

    def insert_records(self, values):
        insert_statement = 'INSERT INTO ' + self.__table_name + ' VALUES('
        for value in values:
            insert_statement += '\'' + value + '\','
        insert_statement = insert_statement.rstrip(',') + ')'
        self.__statement = insert_statement
        return self.__execute_query()

    def update_records(self, current_values={}, update_values={}):
        update_statement = 'UPDATE ' + self.__table_name + ' SET '
        for key, value in update_values.items():
            update_statement += key + '=\'' + value + '\' AND '
        update_statement = update_statement.rstrip(' AND ') + ' WHERE '
        for key, value in current_values.items():
            update_statement += key + '=\'' + value + '\' AND '
        update_statement = update_statement.rstrip(' AND ')
        self.__statement = update_statement
        return self.__execute_query()

    def delete_records(self, values={}):
        delete_statement = 'DELETE FROM ' + self.__table_name + ' WHERE '
        for key, value in values.items():
            delete_statement += key + '=\'' + value + '\' AND '
        delete_statement = delete_statement.rstrip(' AND ')
        self.__statement = delete_statement
        return self.__execute_query()

    def __create_table(self, columns):
        create_statement = 'CREATE TABLE ' + 'transfer_records' + ' ('
        for column, data_type, constraint in columns:
            create_statement += column + ' ' + data_type + ' ' + constraint + ','
        create_statement = create_statement.rstrip(',')
        create_statement += ')' + ";"
        self.__statement = create_statement
        print(self.__table__name + ' created')
        return self.__execute_query()


    '''def __set_columns(self, columns):  # When columns are not hard-coded
        get_columns_query = 'PRAGMA table_info(' + self.__table_name + ')'
        self.__statement = get_columns_query
        rows = self.__execute_query()
        rows = [row[0] for row in rows]
        self.__columns = columns'''