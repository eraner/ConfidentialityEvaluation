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
                    FOREIGN KEY(role) REFERENCES Roles(name)
                    );"""
    execute_query(sql_command)

# Add Users
    sql_command = """INSERT INTO Users (id, u_name, role)
        VALUES (NULL, "Eran Laudin", "Manager"),
                (NULL, "Ohad Cohen", "Cleaner"),
                (NULL, "Nir Levi", "Developer"),
                (NULL, "Omri Koresh", "QA"),
                (NULL, "Yael Gershenshtein", "Guard");"""
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


def delete_role(role, main_window):
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()
    query = "DELETE FROM Roles WHERE name= \"" + role + "\";"
    cur.execute(query)
    conn.commit()
    main_window.print_to_log("Database", role + " was removed")


def add_role(role, rank, main_window):
    """
    Insert new role to Database
    :param role:
    :return:
    """
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()
    query = "INSERT INTO Roles (name, rank)" + \
            "VALUES (\""+role+"\", "+rank+")"
    try:
        cur.execute(query)
        conn.commit()
        return True
    except Exception as e:
        main_window.print_to_log("Database", "Something went wrong..\n" + str(e))
        return False


def add_user(username, role, main_window):
    """
    Insert new user to Database
    :param username:
    :param role:
    :return: True when success, False when fail.
    """
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE u_name=\"" + username+"\";")
    rows = cur.fetchall()
    if len(rows) != 0:
        main_window.print_to_log("Database", "username already exists!")
        return False

    cur.execute("SELECT * FROM Roles WHERE name=\"" + role + "\";")
    rows = cur.fetchall()
    if len(rows) == 0:
        main_window.print_to_log("Database", "Invalid role!")
        return False

    query = "INSERT INTO Users (id, u_name, role)" + \
            "VALUES (NULL, \""+username+"\", \""+role+"\")"

    cur.execute(query)
    conn.commit()
    return True


def delete_user(username, main_window):
    """
    remove user from Database
    :param username:
    :return:
    """
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE u_name=\"" + username + "\";")
    rows = cur.fetchall()
    if len(rows) == 0:
        main_window.print_to_log("Database", "username doesn't exist!")
        return False
    query = "DELETE FROM Users WHERE u_name= \"" + username + "\";"
    cur.execute(query)
    conn.commit()
    return True


def add_resource(name, r_type, main_window):
    """
    add resource to table.
    :param name:
    :param r_type:
    :return:
    """
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()
    query = "INSERT INTO Resources (id, name, type)" + \
            "VALUES (NULL, \""+name+"\", \""+r_type+"\")"
    try:
        cur.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print "Something went wrong..\n" + str(e)
        return False

def delete_resource_by_id(id, main_window):
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Resources WHERE id=" + id + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        print "resource doesn't exist!"
        return False
    query = "DELETE FROM Resources WHERE id= " + id + ";"
    cur.execute(query)
    conn.commit()
    return True


def add_rule(role, resource_id, permissions, main_window):
    """
    Check validity of params and insert rule to DB.
    :param role:
    :param resource_id:
    :param permissions:
    :return:
    """
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM Resources WHERE id=" + resource_id + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        main_window.print_to_log("Database", "resource doesn't exist!")
        return False
    cur.execute("SELECT * FROM Roles WHERE name=\"" + role + "\";")
    rows = cur.fetchall()
    if len(rows) == 0:
        main_window.print_to_log("Database", "Invalid role!")
        return False

    query = "INSERT INTO Rules(role, resource_id, permissions) VALUES" \
            "(\"" + role + "\", " + resource_id + ", \"" + permissions + "\");"
    cur.execute(query)
    conn.commit()
    return True


def delete_rule(role, resource_id, main_window):
    conn = create_connection("Utils\\Database\\auth.db")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Resources WHERE id=" + resource_id + ";")
        rows = cur.fetchall()
    except Exception as e:
        main_window.print_to_log("Database", str(e))
        return False
    if len(rows) == 0:
        main_window.print_to_log("Database", "resource doesn't exist!")
        return False

    cur.execute("SELECT * FROM Roles WHERE name=\"" + role + "\";")
    rows = cur.fetchall()
    if len(rows) == 0:
        main_window.print_to_log("Database", "Invalid role!")
        return False

    query = "DELETE FROM Rules WHERE resource_id= " + resource_id + " AND role= \"" + role + "\";"
    cur.execute(query)
    conn.commit()
    return True


def fetch_table(conn, table_name):
    """
    Query all rows in the requested table
    :param conn: the Connection object
            table_name: The requested table name to pull from DB
    :param table_name:
    :return: rows of requested table
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table_name + ";")

    rows = cur.fetchall()

    return rows


def print_authorization_system(main_window):
    con = create_connection("Utils\\Database\\auth.db")

    """Print Users Table"""
    main_window.print_to_log("DBHelper", "-"*10 + "Getting all Users" + "-"*10)
    allUsers = get_all_users(con)
    for user in allUsers:
        main_window.print_to_log("DBHelper", "[" + str(user[0]) + ". Username: " + user[1] + ", Role: " + user[2] + " ]")

    """Print Roles Table"""
    main_window.print_to_log("DBHelper", "-"*10 + "Getting all Roles" + "-"*10)
    allRoles = get_all_roles(con)
    for role in allRoles:
        main_window.print_to_log("DBHelper", "[ Name: " + role[0] + ", Type: " + str(role[1]) + " ]")

    """Print Resources Table"""
    main_window.print_to_log("DBHelper", "-"*10 + "Getting all Resources" + "-"*10)
    allResources = get_all_resources(con)
    for resource in allResources:
        main_window.print_to_log("DBHelper", "[ " + str(resource[0]) + ". Name: " + resource[1] + ", Type: " + resource[2] + " ]")

    """Print Rules Table"""
    main_window.print_to_log("DBHelper", "-"*10 + "Getting all Rules" + "-"*10)
    allRules = get_all_rules(con)
    for rule in allRules:
        main_window.print_to_log("DBHelper", "[ Role: " + rule[0] + ", ResourceID: " + str(rule[1]) + " --> " + rule[2] + " ]")

    con.close()


if __name__ == "__main__":
    connection = create_connection("auth.db")

    db_init()

    connection.close()
