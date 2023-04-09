import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (user_id, first_name, second_name, age, email, pswd, access_id_FK) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Nikita', 'Kulichev', '20', 'longrast.2002@gmail.com', 'ff1', '1')
            )

cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('1', '1')
            )

cur.execute("INSERT INTO user (user_id, first_name, second_name, age, email, pswd, access_id_FK) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('2', 'Custom', 'Customer', '20', 'longrast.2002@gmail.com', 'ff2', '2')
            )

cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('2', '2')
            )

connection.commit()
connection.close()