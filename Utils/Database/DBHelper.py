__author__ = 'eranlaudin'


import sqlite3

connection = sqlite3.connect("auth.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE employee;""")

sql_command = """CREATE TABLE employee
(staff_number INTEGER PRIMARY KEY,fname VARCHAR(20),lname VARCHAR(30),
gender CHAR(1),joining DATE,birth_date DATE);"""



cursor.execute(sql_command)

connection.commit()

connection.close()