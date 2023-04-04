import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (user_id, first_name, second_name, age, email, pswd, access_lvl) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Nikita', 'Kulichev', '20', 'longrast.2002@gmail.com', 'Qwertyui1!', '1')
            )

cur.execute("INSERT INTO user (user_id, first_name, second_name, age, email, pswd, access_lvl) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('2', 'Custom', 'Customer', '20', 'longrast.2002@gmail.com', 'Qwertyui2!', '2')
            )

connection.commit()
connection.close()