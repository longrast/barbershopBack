import sqlite3
import os

#удаление всех фоток пользователей, кроме дефолтной
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

cur.execute("INSERT INTO users (user_id, first_name, second_name, age, number, email, pswd, pic_name_u) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Nikita', 'Kulichev', '20', '+7 (900) 999-11-11', 'longrast.2002@gmail.com', 'ffff1111', 'unauthorized_user.png')
            )
cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('1', '2')
            )
cur.execute("INSERT INTO users (user_id, first_name, second_name, age, number, email, pswd, pic_name_u) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('2', 'Sonya', 'Shushnaeva', '20', '+7 (900) 999-55-55', 'ssonchass@mail.ru', 'ff2', 'unauthorized_user.png')
            )
cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('2', '2')
            )
cur.execute("INSERT INTO masters (master_id, first_name, second_name, patronymic_name, experience, description, pic_name_m) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Илья', 'Савин', 'Игоревич', '20', 'Круто стрижет', 'portfolio_master1.png')
            )
cur.execute("INSERT INTO masters (master_id, first_name, second_name, patronymic_name, experience, description, pic_name_m) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('2', 'Григорий', 'Лосев', 'Абрахамович', '20', 'Стрижет не хуже Ильи Игоревича', 'portfolio_master3.png')
            )
cur.execute("INSERT INTO reviews (review_id, reviewer_id, master_id, rating, comments) VALUES (?, ?, ?, ?, ?)",
            ('1', '1', '1', '5', 'Ощень харашо сделяль')
            )
cur.execute("INSERT INTO reviews (review_id, reviewer_id, master_id, rating, comments) VALUES (?, ?, ?, ?, ?)",
            ('2', '1', '2', '5', 'Ощень харашо сделяль')
            )
cur.execute("INSERT INTO reviews (review_id, reviewer_id, item_id, rating, comments) VALUES (?, ?, ?, ?, ?)",
            ('3', '1', '1', '5', 'Ощень харашо для ног')
            )
cur.execute("INSERT INTO reviews (review_id, reviewer_id, item_id, rating, comments) VALUES (?, ?, ?, ?, ?)",
            ('4', '2', '3', '5', 'Ощень харашо для рук')
            )
cur.execute("INSERT INTO items (item_id, item_category, item_name, item_description, item_price, item_amount, pic_name_i) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('1', '1', 'Масло для бороды №1', 'Масло для ухода за бородой №1', '500', '55', 'default_item.png')
            )
cur.execute("INSERT INTO items (item_id, item_category, item_name, item_description, item_price, item_amount, pic_name_i) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('3', '1', 'Масло для бороды №2', 'Масло для ухода за бородой №2', '500', '55', 'default_item.png')
            )
cur.execute("INSERT INTO items (item_id, item_category, item_name, item_description, item_price, item_amount, pic_name_i) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('2', '2', 'Пена для бритья', 'Пена с оптимальной консистенцией для гладкого бритья', '500', '55', 'pena_dlya_britya.jpg')
            )
cur.execute("INSERT INTO services (service_id, service_name, service_price, pic_name_s) VALUES (?, ?, ?, ?)",
            ('1', 'Стрижка', '500', 'service_and_price1.jpg')
            )
cur.execute("INSERT INTO services (service_id, service_name, service_price, pic_name_s) VALUES (?, ?, ?, ?)",
            ('2', 'Бритье', '500', 'service_and_price1.jpg')
            )

'''
cur.execute("INSERT INTO users (user_id, first_name, second_name, age, number, email, pswd, pic_name_u) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('1', 'Nikita', 'Kulichev', '20', '+7 (900) 999-11-11', 'longrast.2002@gmail.com', 'ff1', 'unauthorized_user.png')
            )

cur.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
            ('1', '1')
            )

'''




connection.commit()
connection.close()