import sqlite3
from sqlite3 import Error


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
                (NULL, "Ohad Cohen", "Cleaner", "2017-11-02", "1965-05-20"),
                (NULL, "Nir Levi", "Developer", "2017-12-01", "1990-04-15"),
                (NULL, "Omri Koresh", "QA", "2017-10-01", "1990-04-18"),
                (NULL, "Yael Gershenshtein", "Guard", "2017-09-01", "1992-04-15");"""
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
    execute_query(sql_command)

# Create Rules table
    sql_command = """CREATE TABLE Rules
                    (role VARCHAR(40),
                    resource_id INTEGER,
                    permissions VARCHAR(10),
                    FOREIGN KEY(role) REFERENCES Roles(name)
                    FOREIGN KEY(resource_id) REFERENCES Resources(id)
                    );"""
    execute_query(sql_command)

# Add Rules
    sql_command = """INSERT INTO Rules (role, resource_id, permissions) VALUES
                    ("Manager", 2, "rw"),
                    ("Developer", 1, "rw"),
                    ("Cleaner", 3, "r");
                    """
    execute_query(sql_command)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def get_all_resources(conn):
    """
    Query all rows in the Resources table
    :param conn: the Connection object
    :return:
    """
    return fetch_table(conn, "Resources")


def get_all_roles(conn):
    """
    Query all rows in the Roles table
    :param conn: the Connection object
    :return:
    """
    return fetch_table(conn, "Roles")


def get_all_users(conn):
    """
    Query all rows in the Users table
    :param conn: the Connection object
    :return:
    """
    return fetch_table(conn, "Users")


def get_all_rules(conn):
    """
    Query all rows in the Rules Table
    :param conn:
    :return:
    """
    return fetch_table(conn, "Rules")


def insert_user(conn, username, role, join_date, birth_date):
    """
    Insert new user to Database
    :param conn:
    :param username:
    :param role:
    :param join_date:
    :param birth_date:
    :return: True when success, False when fail.
    """
    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE u_name=" + username+";")
    rows = cur.fetchall()
    if len(rows) != 0:
        print "username already exists!"
        return False

    cur.execute("SELECT * FROM Roles WHERE name=" + role + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        print "Invalid role!"
        return False

    """TODO: validate dates legal"""

    query = "INSERT INTO Users (id, u_name, role, joining, birth_date)" + \
            "VALUES (NULL, \""+username+"\", \""+role+"\", \""+join_date+"\", \""+birth_date+"\")"
    execute_query(query)
    return True


def fetch_table(conn, table_name):
    """
    Query all rows in the requested table
    :param conn: the Connection object
            table_name: The requested table name to pull from DB
    :return: rows of requested table
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table_name + ";")

    rows = cur.fetchall()

    return rows


def print_authorization_system():
    con = create_connection("Utils\\Database\\auth.db")

    """Print Users Table"""
    print("\n" + "-"*10 + "Getting all Users" + "-"*10)
    allUsers = get_all_users(con)
    for user in allUsers:
        print(user)

    """Print Roles Table"""
    print("\n" + "-"*10 + "Getting all Roles" + "-"*10)
    allRoles = get_all_roles(con)
    for role in allRoles:
        print(role)

    """Print Rules Table"""
    print("\n" + "-"*10 + "Getting all Rules" + "-"*10)
    allRules = get_all_rules(con)
    for role in allRules:
        print(role)

    """Print Resources Table"""
    print("\n" + "-"*10 + "Getting all Resources" + "-"*10)
    allResources = get_all_resources(con)
    for resource in allResources:
        print(resource)

    con.close()


if __name__ == "__main__":
    connection = create_connection("auth.db")

    db_init()

    connection.close()
