import sqlite3
import random
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from datetime import timedelta
from flask_mail import Mail, Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

import re
import smtplib
import dns.resolver
import socket

import uuid
import os


def get_db_connection():
    '''
    Инициализирует БД и предоставляет возможность обращаться с бд посредством кортежа.

    :return: Объект для возвращения данных в виде кортежа.
    :rtype: Object sqlite3.Row

    '''
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#для проверки работы нужно обновить код приложения
def send_email(message="Пустое сообщение", subject="Пустая тема", sender="longrast.2002@gmail.com", recipient="longrast.2002@gmail.com"):
    '''Подключается к SMTP серверу и совершает попытку отправки сообщения.
    
    :param message: Значение по умолчанию "Пустое сообщение".
    :type message: str
    :param subject: Значение по умолчанию "Пустая тема".
    :type subject: str
    :param sender: Значение по умолчанию "longrast.2002@gmail.com".
    :type sender: str
    :param recipient: Значение по умолчанию "longrast.2002@gmail.com".
    :type recipient: str
    :raise _ex: Если сообщение так и не было отправлено.
    :return: Успешность выполнения операции.
    :rtype: bool

    '''
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    #bmyz!ebet!flfv!lhli
    msg.attach(MIMEText(message, 'plain')) #MIMEText(message, 'plain')
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    
    server.set_debuglevel(1)
    try:
        server.login("longrast.2002@gmail.com", "***")
        server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
        print("Message was sent")
        return True
    except Exception as _ex:
        print("Message wasn't sent")
        return False
    
    
'''
def send_email(message, recipient): #через регулярку проверка домена почты и в зависимости от нее указывать smtp.mail.ru 465 или smtp.gmail.com 587, так же надо запросить сервер для smtp.mail
    acc = "longrast.2002@gmail.com"
    #recipient = "godfather200215@gmail.com"
    password = "heugbfwqweyamzwu" #Необходимо создать новый пароль приложения
    server = smtplib.SMTP("smtp.gmail.com", 587) #465 для ssl
    server.ehlo()
    server.starttls()
    server.set_debuglevel(1)
    try:
        server.login(acc, password)
        msg = MIMEText(message, 'plain', 'utf-8')
        print(msg)
        print("\n"+msg.as_string())
        server.sendmail(acc, recipient, msg.as_string()) #sender, recipient, msg
        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")
        print("Message was sent")
        return True
    except Exception as _ex:
        print("Message wasn't sent")
        return False
  
'''
  
'''
def recieve_email(message, sender):
    login = "longrast.2002@gmail.com"
    #sender = "longrast.2002@gmail.com"
    recipient = "longrast.2002@gmail.com"
    password = "heugbfwqweyamzwu" #Необходимо создать новый пароль приложения

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header('subject-example', 'utf-8')
    msg['From'] = sender
    msg['To'] = recipient

    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)

    try:
        server.starttls()
        server.login(login, password)
        print("sent1")
        server.sendmail(sender, recipient, msg.as_string()) #sender, recipient, msg
        print("sent2")
        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")
        server.quit()
        return True
    except Exception as _ex:
        print("sent3")
        server.quit()
        return False

'''


def check_if_email_exists(email): #работает только для gmail
    '''Проверяет введенный пользователем адрес на существование.
    
    :param email: На вход подается адрес почты.
    :type kind: str
    :return: Успешность выполнения операции.
    :rtype: bool
    
    '''
    email_address = email

    #Step 1: Check email
    #Check using Regex that an email meets minimum requirements, throw an error if not
    addressToVerify = email_address
    match = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$', addressToVerify)

    if match == None:
        flash('Возможно, вы неправильно ввели адрес ', 'error')
        return False

    #Step 2: Getting MX record
    #Pull domain name from email address
    domain_name = email_address.split('@')[1]

    #get the MX record for the domain
    records = dns.resolver.query(domain_name, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    #Step 3: ping email server
    #check if the email address exists

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('longrast.2002@gmail.com')
    code, message = server.rcpt(str(email_address))
    server.quit()

    # Assume 250 as Success
    if code == 250:
        print('Y')
        return True
    else:
        print('N')
        return False



app = Flask(__name__)
app.secret_key = 'verystrongsecretkey'
app.permanent_session_lifetime = timedelta(minutes=5)


'''
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'longrast.2002@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'longrast.2002@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'xldqywyphzrjbafr'  # введите пароль xldqywyphzrjbafr
'''

#-------------------------------------------------------------------------------------------------------------

@app.route("/")
def home():
    '''Отображает главную страницу
    
    :return: Отображение страницы.
    :rtype: str

    '''
    return render_template('home.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/registration", methods=('GET', 'POST'))
def registration():
    '''Считывает данные введенные в форму и формирует запрос к БД на добавление нового пользователя с соответствующими правами.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        age = request.form['age']
        number = request.form['number']
        email = request.form['email']
        pswd = request.form['pswd']

        profile_pic = request.files["profile_pic"]

        if not email or not pswd:
            flash('Пожалуйста, заполните формы', 'error')
        elif not check_if_email_exists(email):
            flash('Такой почты не существует', 'error')
        else:
            if profile_pic:
                pic_name_u = str(uuid.uuid1()) + os.path.splitext(profile_pic.filename)[1]
                profile_pic.save(os.path.join("static/images_users", pic_name_u))
            else:
                pic_name_u = None

            #session["name"] = first_name
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()
            if check_table_user_id:
                conn.close()
                flash('Вы уже зарегистрированы!', 'error')
                return redirect(url_for('authorization'))
            if pic_name_u:
                conn.execute('INSERT INTO users (first_name, second_name, age, number, email, pswd, pic_name_u) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (first_name, second_name, age, number, email, pswd, pic_name_u))
                table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()['user_id']
                conn.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
                    (table_user_id, '2'))
            else:
                conn.execute('INSERT INTO users (first_name, second_name, age, number, email, pswd) VALUES (?, ?, ?, ?, ?, ?)',
                    (first_name, second_name, age, number, email, pswd))
                table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()['user_id']
                conn.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
                    (table_user_id, '2'))
            conn.commit()
            conn.close()
            flash("Вы успешно зарегистрированы", "noerror")
            send_email("Вы зарегистрированы", "Регистрация", "longrast.2002@gmail.com", email) #message, subject, sender, recipient
            #return redirect(url_for('authorization'))
    return render_template('registration.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/authorization", methods=('GET', 'POST'))
def authorization():
    '''Считывает данные введенные в форму, формирует запрос к бд для сверки пароля и открывает сессию.
            
    :return: Отображение страницы или перенаправление.
    :rtype: str

    '''
    if request.method == 'POST':
        email = request.form['email']
        pswd = request.form['pswd']
        if not email or not pswd:
            flash('Пожалуйста, заполните формы', 'error')
        else:
            #session["name"] = first_name
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()
            if not check_table_user_id:
                flash('Такая почта не найдена!', 'error')
                return redirect(url_for('authorization'))
            else:
                table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()['user_id']
                table_first_name = conn.execute('SELECT first_name FROM users where email = ?', (email,)).fetchone()['first_name']
                table_second_name = conn.execute('SELECT second_name FROM users where email = ?', (email,)).fetchone()['second_name']
                table_age = conn.execute('SELECT age FROM users where email = ?', (email,)).fetchone()['age']
                table_number = conn.execute('SELECT number FROM users where email = ?', (email,)).fetchone()['number']
                table_email = conn.execute('SELECT email FROM users where email = ?', (email,)).fetchone()['email']
                table_pswd = conn.execute('SELECT pswd FROM users where email = ?', (email,)).fetchone()['pswd']
                table_pic_name = conn.execute('SELECT pic_name_u FROM users where email = ?', (email,)).fetchone()['pic_name_u']
                #check = conn.execute('SELECT * FROM users where email = ?', (email,)).fetchone()['pswd']
                conn.close()
                #print(table_pswd)
                #print(pswd)
                #print(check)
                if table_pswd == pswd:
                    session["user_id"] = table_user_id
                    session["first_name"] = table_first_name
                    session["second_name"] = table_second_name
                    session["age"] = table_age
                    session["number"] = table_number
                    session["email"] = table_email
                    session["pswd"] = table_pswd
                    session["pic_name_u"] = table_pic_name
                    conn = get_db_connection()
                    conn.execute('INSERT INTO shopping_session (user_id) VALUES (?)', (str(session["user_id"])))
                    conn.commit()
                    table_shopping_session = conn.execute('SELECT * FROM shopping_session WHERE user_id = ? ORDER BY shop_session_id DESC', (str(session["user_id"]))).fetchone()["shop_session_id"]
                    conn.close()
                    session["shopping_session"] = table_shopping_session
                    print(f"shopping session id {table_shopping_session}")
                    session.permanent = True
                    return redirect(url_for('home'))
                else:
                    flash('Неверный пароль', 'error')
                    return redirect(url_for('authorization'))
    return render_template('authorization.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/restore_email", methods=('GET', 'POST'))
def restore_email():
    '''Считывает данные введенные в форму, формирует запрос к БД на поиск почты, если такая есть отправляет на почту сообщение с проверочным кодом.
                
    :return: Отображение страницы или перенаправление.
    :rtype: str

    '''
    if request.method == 'POST':
        email = request.form['email']
        if not email:
            flash('Пожалуйста, заполните формы', 'error')
        else:
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()
            if not check_table_user_id:
                flash('Такая почта не найдена!', 'error')
                return redirect(url_for('restore_email'))
            else:
                table_email = conn.execute('SELECT email FROM users where email = ?', (email,)).fetchone()['email']
                table_pswd = conn.execute('SELECT pswd FROM users where email = ?', (email,)).fetchone()['pswd']
                conn.close()
                x = random.randint(0,9999)
                message = "Код - " + str(x)
                send_email(message, "Восстановление пароля", "longrast.2002@gmail.com", table_email) #message, subject, sender, recipient
                print("sent")
                session["email"] = table_email
                session["pswd"] = table_pswd #сессия хранится как зашифрованные куки, так что с безопасностью все должно быть неплохо
                session["x"] = x
                session.permanent = True
                return redirect(url_for('restore_password'))
    return render_template('restore-email.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/restore_password", methods=('GET', 'POST'))
def restore_password():
    '''Считывает данные введенные в форму и, если введен верный код, отправляет на почту сообщение с паролем.
                
    :return: Отображение страницы.
    :rtype: str

    '''
    flash("Код был выслан на почту", "noerror")
    if request.method == 'POST':
        session['_flashes'].clear()
        code = request.form['code']
        if str(code) == str(session["x"]):
            flash("Ваш пароль отправлен на почту", "noerror")
            password = str(session["pswd"])
            message = "Ваш пароль - " + password
            send_email(message, "Пароль", "longrast.2002@gmail.com", session["email"]) #message, subject, sender, recipient
        else:
            flash("Ваш код неправильный, проверьте почту еще раз", 'error')
            x = random.randint(0,9999)
            message = "Код - " + str(x)
            send_email(message, "Восстановление пароля", "longrast.2002@gmail.com", session["email"]) #message, subject, sender, recipient
            session["x"] = x
    return render_template('restore-password.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/contacts", methods=('GET', 'POST'))
def contacts():
    '''Считывает данные введенные в форму и отправляет сообщение на почту с введенными данными.
                
    :return: Отображение страницы или перенаправление.
    :rtype: str

    '''
    if request.method == 'POST':
        name = request.form["first_name"]
        email = request.form['email']
        area = request.form['area']
        message = area
        send_email(message, f"Сообщение от пользователя: {name}", email, "longrast.2002@gmail.com") #message, subject, sender, recipient
        print(email)
        return redirect(url_for('contacts'))
    return render_template('contacts.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/profile")
def profile():
    '''Отображает профиль пользователя, если он авторизован.
        
    :return: Отображение страницы или сообщение об ошибке.
    :rtype: str, для ошибки int

    '''
    if session.get("user_id"):
        return render_template('profile.html')
    else:
        return abort(404)

#-------------------------------------------------------------------------------------------------------------

@app.route("/profile_edit", methods=('GET', 'POST'))
def profile_edit():
    '''Предоставляет функционал для изменения профиля пользователя, если он авторизован.
                
    :return: Отображение страницы, перенаправление или сообщение об ошибке.
    :rtype: str, для ошибки int

    '''
    if session.get("user_id"):
        print("ок11")
        if request.method == 'POST':
            print("ок22")
            if session.get("_flashes"):
                session['_flashes'].clear()
            print("ок33")
            first_name = request.form['first_name']
            second_name = request.form['second_name']
            age = request.form['age']
            number = request.form['number']
            print("ок44")
            email = request.form['email']
            #pswd = request.form['pswd']
            print("ок55")
            profile_pic = request.files["profile_pic"]
            print("ок66")
            if not email:
                flash('Пожалуйста, заполните формы', 'error')
            elif not check_if_email_exists(email):
                flash('Такой почты не существует', 'error')
            else:
                print("ок33")
                conn = get_db_connection()
                check_table_email = conn.execute('SELECT email FROM users where user_id = ?', (session["user_id"],)).fetchone()["email"]
                if email != check_table_email:
                    print("надо проверить")
                    check_table_user_id = conn.execute('SELECT user_id FROM users where email = ?', (email,)).fetchone()
                    if check_table_user_id:
                        conn.close()
                        flash('Данная почта уже используется', 'error')
                        return redirect(url_for('profile_edit'))
                    else:
                        print("ок44")
                        if profile_pic:
                            check_table_pic_name = conn.execute('SELECT pic_name_u FROM users where user_id = ?', (session["user_id"],)).fetchone()["pic_name_u"]
                            if check_table_pic_name != "unauthorized_user.png":
                                os.remove(f"static/images_users/{check_table_pic_name}")
                            print(check_table_pic_name)
                            pic_name_u = str(uuid.uuid1()) + os.path.splitext(profile_pic.filename)[1]
                            profile_pic.save(os.path.join("static/images_users", pic_name_u))
                            print("ок1")
                        else:
                            pic_name_u = None

                        if profile_pic:
                            print("ок2")
                            conn.execute('UPDATE users SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pic_name_u = ? WHERE user_id = ?',
                                (first_name, second_name, age, number, email, pic_name_u, session["user_id"]))
                            session["pic_name_u"] = pic_name_u
                            print("ок3")
                        else:
                            conn.execute('UPDATE users SET first_name = ?, second_name = ?, age = ?, number = ?, email = ? WHERE user_id = ?',
                                (first_name, second_name, age, number, email, session["user_id"]))
                            check_table_pic_name = conn.execute('SELECT pic_name_u FROM users where user_id = ?', (session["user_id"],)).fetchone()["pic_name_u"]
                            session["pic_name_u"] = check_table_pic_name
                        conn.commit()
                        conn.close()
                        flash("Данные внесены", "noerror")
                        session["first_name"] = first_name
                        session["second_name"] = second_name
                        session["age"] = age
                        session["number"] = number
                        session["email"] = email
                        #session["pswd"] = pswd
                        return redirect(url_for('profile'))
                else:

                    if profile_pic:
                        check_table_pic_name = conn.execute('SELECT pic_name_u FROM users where user_id = ?', (session["user_id"],)).fetchone()["pic_name_u"]
                        if check_table_pic_name != "unauthorized_user.png":
                            os.remove(f"static/images_users/{check_table_pic_name}")
                        print(check_table_pic_name)
                        pic_name_u = str(uuid.uuid1()) + os.path.splitext(profile_pic.filename)[1]
                        profile_pic.save(os.path.join("static/images_users", pic_name_u))
                    else:
                        pic_name_u = None

                    if profile_pic:
                        conn.execute('UPDATE users SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pic_name_u = ? WHERE user_id = ?',
                            (first_name, second_name, age, number, email, pic_name_u, session["user_id"]))
                        session["pic_name_u"] = pic_name_u
                    else:
                        conn.execute('UPDATE users SET first_name = ?, second_name = ?, age = ?, number = ?, email = ? WHERE user_id = ?',
                            (first_name, second_name, age, number, email, session["user_id"]))
                        check_table_pic_name = conn.execute('SELECT pic_name_u FROM users where user_id = ?', (session["user_id"],)).fetchone()["pic_name_u"]
                        session["pic_name_u"] = check_table_pic_name
                    conn.commit()
                    conn.close()
                    flash("Данные внесены", "noerror")
                    session["first_name"] = first_name
                    session["second_name"] = second_name
                    session["age"] = age
                    session["number"] = number
                    session["email"] = email
                    return redirect(url_for('profile'))
        return render_template('profile_edit.html')
    else:
        return abort(404)

#-------------------------------------------------------------------------------------------------------------

@app.route("/logout")
def logout():
    '''Предоставляет возможность закрыть сессию.
            
    :return: Перенаправление на главную страницу.
    :rtype: str

    '''
    session.clear()
    return redirect(url_for('home'))

#-------------------------------------------------------------------------------------------------------------

@app.route("/change_pswd", methods=('GET', 'POST'))
def change_pswd():
    '''Предоставляет возможность изменить пароль пользователю.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    if session.get("user_id"):
        if request.method == 'POST':
            old_pswd = request.form['old_pswd']
            new_pswd = request.form['new_pswd']
            conn = get_db_connection()
            table_old_pswd = conn.execute('SELECT pswd FROM users WHERE user_id = ?', (session["user_id"],)).fetchone()["pswd"]
            if table_old_pswd == old_pswd:
                conn.execute('UPDATE users SET pswd = ? WHERE user_id = ?',
                            (new_pswd, session["user_id"]))
                conn.commit()
                conn.close()
                print(new_pswd)
                flash("Данные внесены", "noerror")
            else:
                flash("Старый пароль введен неправильно", "error")
                redirect(url_for('home'))
    else:
        return abort(404)
    return render_template('change-pswd.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/portfolio")
def portfolio():
    '''Отображает всех мастеров салона.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    conn = get_db_connection()
    masters = conn.execute('SELECT * FROM masters').fetchall()
    return render_template('portfolio.html', masters=masters)

#-------------------------------------------------------------------------------------------------------------

@app.route("/master-<int:master_id>")
def portfolio_card(master_id):
    '''Отображает детальное описание конкретного мастера, а также комментарии, оставленные пользователями.
         
    :return: Отображение страницы.
    :rtype: str

    '''
    conn = get_db_connection()
    master = conn.execute('SELECT * FROM masters WHERE master_id = ?', (master_id,)).fetchone()
    if master is None:
        abort(404)
    
    table_master_id = conn.execute('SELECT * FROM masters WHERE master_id = ?', (master_id,)).fetchone()['master_id']
    reviews = conn.execute('SELECT * FROM reviews JOIN users ON reviewer_id=user_id WHERE master_id = ?', (table_master_id,)).fetchall()
    session['master_id'] = master_id
    
    

    '''
    print(reviews)
    table_reviewer_id = conn.execute('SELECT * FROM reviews WHERE master_id = ?', (table_master_id,)).fetchone()['reviewer_id']
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (table_reviewer_id,)).fetchall()
    table_user_name = conn.execute('SELECT * FROM users WHERE user_id = ?', (table_reviewer_id,)).fetchone()['first_name']
    print(table_user_name) #решить проблему. мб поможет длинный или вложенный запрос?
    '''
    conn.close()
    return render_template('portfolio-card.html', master=master, reviews=reviews)

#-------------------------------------------------------------------------------------------------------------

@app.route("/add_comments_master", methods=('GET', 'POST'))
def add_comments_master():
    '''Предоставляет интерфейс пользователя для создания комментария и оценки мастеру.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        if session.get("user_id"):
            if not rating or not comments:
                flash('Пожалуйста, заполните формы', 'error')
            #table_user_id = conn.execute('SELECT user_id FROM users where user_id = ?', (session['user_id'],)).fetchone()['user_id']
            conn = get_db_connection()
            conn.execute('INSERT INTO reviews (reviewer_id, master_id, rating, comments) VALUES (?, ?, ?, ?)',
                    (session['user_id'], session['master_id'], rating, comments))
            conn.commit()
            conn.close()
            flash('Данные внесены', 'noerror')
        else:
            flash("Чтобы оставить комментарий, вы должны быть авторизированы", 'error')
    return render_template('add-comments-master.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/cosmetics", methods=('GET', 'POST'))
def cosmetics():
    '''Отображает ассортимент товара, выставленного на продажу.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    if request.method == 'POST':
        if not session.get("shopping_session"):
            flash("Чтобы добавить товар в корзину, вы должны быть авторизированы", 'error')
        else:
            amount = conn.execute('SELECT COUNT(*) FROM items').fetchone()[0]
            print(f"amount {amount}")
            for i in range(1, amount+1):
                table_item_id = conn.execute('SELECT item_id FROM items WHERE item_id = ?', (str(i))).fetchone()['item_id']
                print(f"iteration {table_item_id}")
                print(request.form['action'])
                print(request.form.get(table_item_id))
                if str(table_item_id) in request.form['action']:
                    conn.execute('INSERT INTO carts (shop_session_id_FK, item_id_FK) VALUES (?, ?)', (session["shopping_session"], table_item_id))
                    conn.commit()
                    print("choosed")
                else:
                    pass
    return render_template('cosmetics.html', items=items)

#-------------------------------------------------------------------------------------------------------------

@app.route("/item-<int:item_id>", methods=('GET', 'POST'))
def cosmetics_card(item_id):
    '''Отображает детальное описание конкретного товара.
     
    :return: Отображение страницы.
    :rtype: str
    
    '''
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE item_id = ?', (item_id,)).fetchone()
    if item is None:
        abort(404)
    table_item_id = conn.execute('SELECT * FROM items WHERE item_id = ?', (item_id,)).fetchone()['item_id']
    reviews = conn.execute('SELECT * FROM reviews JOIN users ON reviewer_id=user_id WHERE item_id = ?', (table_item_id,)).fetchall()
    session['item_id'] = item_id

    if request.method == 'POST':
        if not session.get("shopping_session"):
            flash("Чтобы добавить товар в корзину, вы должны быть авторизированы", 'error')
        else:
            conn.execute('INSERT INTO carts (shop_session_id_FK, item_id_FK) VALUES (?, ?)', (session["shopping_session"], request.form['action']))
            conn.commit()
            print("choosed")


    return render_template('cosmetics-card.html', item=item, reviews=reviews)

#-------------------------------------------------------------------------------------------------------------

@app.route("/add_comments_item", methods=('GET', 'POST'))
def add_comments_item():
    '''Предоставляет интерфейс пользователя для создания комментария и оценки товару.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        if session.get("user_id"):
            if not rating or not comments:
                flash('Пожалуйста, заполните формы', 'error')
            #table_user_id = conn.execute('SELECT user_id FROM users where user_id = ?', (session['user_id'],)).fetchone()['user_id']
            conn = get_db_connection()
            conn.execute('INSERT INTO reviews (reviewer_id, item_id, rating, comments) VALUES (?, ?, ?, ?)',
                    (session['user_id'], session['item_id'], rating, comments))
            conn.commit()
            conn.close()
            flash('Данные внесены', 'noerror')
        else:
            flash("Чтобы оставить комментарий, вы должны быть авторизированы", 'error')
    return render_template('add-comments-item.html')

#-------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------

@app.route("/cart", methods=('GET', 'POST'))
def cart():
    '''Отображает содержимое корзины пользователя.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    if session.get("shopping_session"):
        conn = get_db_connection()
        cart_items = conn.execute('SELECT *, COUNT(*) AS item_amount, (item_price * COUNT(*)) AS item_total FROM carts JOIN items ON item_id_FK=item_id JOIN shopping_session ON shop_session_id_FK=shop_session_id WHERE shop_session_id = ? GROUP BY item_id', (str(session["shopping_session"]),)).fetchall()
        catalog = conn.execute('SELECT COUNT(*) FROM items').fetchone()[0]
        print(catalog)
        print(f"request info {request.form.get('increment_item', 100)}") #фигня
        if request.method == 'POST':
            if 'decrement_item' in request.form:
                for i in range(1, catalog+1):
                    if str(i) in request.form['decrement_item']:
                        print(f"minus {i}")
                        conn.execute('DELETE FROM carts WHERE cart_item_id IN (SELECT cart_item_id FROM carts WHERE item_id_FK = ? AND shop_session_id_FK = ? ORDER BY cart_item_id LIMIT 1);', (i, session["shopping_session"]))
                        conn.commit()
                        print("decremented")
                        return redirect(url_for('cart'))
                    else:
                        pass
            if 'increment_item' in request.form:
                for i in range(1, catalog+1):
                    if str(i) in request.form['increment_item']:
                        print(f"plus {i}")
                        conn.execute('INSERT INTO carts (shop_session_id_FK, item_id_FK) VALUES (?, ?)', (session["shopping_session"], i))
                        conn.commit()
                        print("decremented")
                        return redirect(url_for('cart'))
                    else:
                        pass
            if 'remove_item' in request.form:
                for i in range(1, catalog+1):
                    print(f"iteration {i}")
                    print(f"position {i}")
                    print(f"item_id {request.form['remove_item']}") #смотрит value, где указан item_id
                    print(request.form.get(i)) #не помню что это
                    if str(i) in request.form['remove_item']:
                        print(f"yes {i}")
                        conn.execute('DELETE FROM carts WHERE item_id_FK = ? AND shop_session_id_FK = ?', (i, session["shopping_session"]))
                        conn.commit()
                        print("removed")
                        return redirect(url_for('cart'))
                    else:
                        pass
    else:
        cart_items = None
    return render_template('cart.html', cart_items=cart_items)

@app.route("/service_and_price", methods=('GET', 'POST'))
def service_and_price():
    '''Отображает все доступные услуги салона.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()

    if request.method == 'POST':
        if not session.get("shopping_session"):
            flash("Чтобы записаться, вы должны быть авторизированы", 'error')
        else:
            #все перелопатить и продумать страничку записи
            amount = conn.execute('SELECT COUNT(*) FROM items').fetchone()[0]
            print(f"amount {amount}")
            for i in range(1, amount+1):
                table_item_id = conn.execute('SELECT item_id FROM items WHERE item_id = ?', (str(i))).fetchone()['item_id']
                print(f"iteration {table_item_id}")
                print(request.form['action'])
                print(request.form.get(table_item_id))
                if str(table_item_id) in request.form['action']:
                    conn.execute('INSERT INTO carts (shop_session_id_FK, item_id_FK) VALUES (?, ?)', (session["shopping_session"], table_item_id))
                    conn.commit()
                    print("choosed")
                else:
                    pass

    return render_template('service_and_price.html', services=services)


@app.route("/service_events")
def service_events():
    '''Отображает все активные записи на сеансы и текущую, собираемую запись.
        
    :return: Отображение страницы.
    :rtype: str

    '''
    return render_template('service_events.html')


'''
@app.route("/hello")
def hello():
    if "first_name" in session:
        temp = session["first_name"]
        content = "hello, " + temp
    else:
        content = "hello, stranger"
    return content

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

'''