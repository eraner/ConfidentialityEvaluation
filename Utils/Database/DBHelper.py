__author__ = 'eranlaudin'
import sqlite3


def execute_query(sql_command):
    '''
    Gets a query and executes it.
    :param sql_command: query
    :return:
    '''
    cursor = connection.cursor()
    cursor.execute(sql_command)
    connection.commit()


def db_init():
    '''
    Initialize Database.
    :return:
    '''
    # delete
    execute_query("""DROP TABLE Users;""")

    # Create Users table
    sql_command = """CREATE TABLE Users
                    (id INTEGER PRIMARY KEY,
                        name VARCHAR(40),
                        role VARCHAR(20),
                        joining DATE,
                        birth_date DATE);"""
    execute_query(sql_command)

    sql_command = """INSERT INTO Users (id, name, role, joining, birth_date)
        VALUES (NULL, "Eran Laudin", "Manager", "2017-11-02", "1961-10-25");"""
    execute_query(sql_command)


if __name__ == "__main__":
    connection = sqlite3.connect("auth.db")

    db_init()

    connection.close()
