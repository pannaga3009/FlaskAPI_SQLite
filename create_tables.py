import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "Create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
#To create auto incrementing columns "id" we use INTEGER
cursor.execute(create_table)

create_table = "Create table if not exists items (name text, price real)"
#real is decimal
cursor.execute(create_table)

connection.commit()
connection.close()
