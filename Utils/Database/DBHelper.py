import sqlite3

"""
TODO: documentation
"""


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
    execute_query("""DROP TABLE Roles;""")
    execute_query("""DROP TABLE Resources;""")
    execute_query("""DROP TABLE Rules;""")

# Create Users table
    sql_command = """CREATE TABLE Users
                    (id INTEGER PRIMARY KEY,
                    u_name VARCHAR(40),
                    role VARCHAR(40),
                    joining DATE,
                    birth_date DATE,
                    FOREIGN KEY(role) REFERENCES Roles(name)
                    );"""
    execute_query(sql_command)

# Add Users
    sql_command = """INSERT INTO Users (id, u_name, role, joining, birth_date)
        VALUES (NULL, "Eran Laudin", "Manager", "2017-11-02", "1961-10-25"),
                (NULL, "Ohad Cohen", "Cleaner", "2017-11-02", "1965-05-20");"""
    execute_query(sql_command)

# Create Roles table
    sql_command = """CREATE TABLE Roles
                    (name VARCHAR(40) PRIMARY KEY,
                    rank INTEGER
                    );"""
    execute_query(sql_command)

# Add roles
    sql_command = """INSERT INTO Roles (name, rank) VALUES
                    ("Manager", 1),
                    ("Developer", 3),
                    ("QA", 4),
                    ("Team Leader", 2),
                    ("Cleaner", 5),
                    ("Guard", 4);"""
    execute_query(sql_command)


# Create Resources table
    sql_command = """CREATE TABLE Resources
                    (id INTEGER PRIMARY KEY,
                    name VARCHAR(20),
                    type VARCHAR(20)
                    );"""
    execute_query(sql_command)

# Add Resources
    sql_command = """INSERT INTO Resources (id, name, type) VALUES
                    (NULL, "DevCode", "dir"),
                    (NULL, "Salaries", "xlsx"),
                    (NULL, "Public", "dir");
                    """

# Create Rules table
    sql_command = """CREATE TABLE Rules
                    (role VARCHAR(40),
                    id INTEGER,
                    FOREIGN KEY(role) REFERENCES Roles(name)
                    FOREIGN KEY(id) REFERENCES Resources(id)
                    );"""
    execute_query(sql_command)


if __name__ == "__main__":
    connection = sqlite3.connect("auth.db")

    db_init()

    connection.close()
