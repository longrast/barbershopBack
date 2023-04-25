import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
'''
cur.execute("INSERT INTO user (user_id, first_name, second_name, age, number, email, pswd) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Nikita', 'Kulichev', '20', '+7 (900) 999-11-11', 'longrast.2002@gmail.com', 'ff1')
            )

cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('1', '1')
            )
'''



connection.commit()
connection.close()