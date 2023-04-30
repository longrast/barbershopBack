import sqlite3
import os

file_list = os.listdir("static/images_users")
for item in file_list:
    s = os.path.join("static/images_users", item)
    if str(os.path.basename(s)).endswith('unauthorized_user.png'):
        pass
    else:
        os.remove(s)
#os.remove(f"static/images_users/{check_table_pic_name}")
connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
'''
cur.execute("INSERT INTO user (user_id, first_name, second_name, age, number, email, pswd, pic_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Nikita', 'Kulichev', '20', '+7 (900) 999-11-11', 'longrast.2002@gmail.com', 'ff1', 'unauthorized_user.png')
            )

cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('1', '1')
            )
'''



connection.commit()
connection.close()