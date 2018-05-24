import sqlite3
from sqlite3 import Error
import datetime


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
        print e

    return None


def evaluate_prediction(app_list, main_window):
    prediction_factor = 0.0
    conn = create_connection("Utils\\HistoryManagement\\history.db")
    cur = conn.cursor()

    query = "SELECT * FROM History ORDER BY date DESC LIMIT 1;"

    cur.execute(query)

    rows = cur.fetchall()
    if len(rows) == 0:
        return 0

    last_apps = rows[0][1].split(",")
    for curr_app in app_list:
        if curr_app in last_apps:
            main_window.print_to_log("HistoryManagement", "Found an app which was in the previews algorithm! "
                                                          "( " + curr_app + " )")
            prediction_factor += 0.3

    return 10 if prediction_factor*10 >= 10 else prediction_factor*10


def insert_result_to_DB(result, app_list, main_window):
    apps = ""
    for app in app_list:
        apps += app + ","

    if len(app_list) > 0:
        apps = apps[0:-1]

    conn = create_connection("Utils\\HistoryManagement\\history.db")
    cur = conn.cursor()

    query = "INSERT INTO History (damage_score, app_names, date)"
    query += "VALUES (" + str(result) + ", \"" + apps + "\", datetime('now'));"

    cur.execute(query)
    conn.commit()
    main_window.print_to_log("HistoryManagement", "Inserted results: " + str(result) + " " + apps)


def history_init():
    conn = create_connection("history.db")
    cur = conn.cursor()

    # query = "DROP TABLE History;"
    # cur.execute(query)
    # conn.commit()

    query = """CREATE TABLE History
                    (damage_score INTEGER,
                    app_names VARCHAR(40),
                    date VARCHAR(40)
                    );"""

    cur.execute(query)
    conn.commit()


if __name__ == '__main__':
    history_init()

