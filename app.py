import sqlite3
import random
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from datetime import timedelta
from flask_mail import Mail, Message #говно не работает
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
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#для проверки работы нужно обновить код приложения
def send_email(message="Пустое сообщение", subject="Пустая тема", sender="longrast.2002@gmail.com", recipient="longrast.2002@gmail.com"):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    #msg_body = "изи пизи лемон сквизи"
    msg.attach(MIMEText(message, 'plain')) #MIMEText(message, 'plain')
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    
    server.set_debuglevel(1)
    try:
        server.login("longrast.2002@gmail.com", "heugbfwqweyamzwu")
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
    return render_template('home.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/registration", methods=('GET', 'POST'))
def registration():
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
                pic_name = str(uuid.uuid1()) + os.path.splitext(profile_pic.filename)[1]
                profile_pic.save(os.path.join("static/images_users", pic_name))
            else:
                pic_name = None

            #session["name"] = first_name
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
            if check_table_user_id:
                conn.close()
                flash('Вы уже зарегистрированы!', 'error')
                return redirect(url_for('authorization'))
            if pic_name:
                conn.execute('INSERT INTO user (first_name, second_name, age, number, email, pswd, pic_name) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (first_name, second_name, age, number, email, pswd, pic_name))
                table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()['user_id']
                conn.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
                    (table_user_id, '2'))
            else:
                conn.execute('INSERT INTO user (first_name, second_name, age, number, email, pswd) VALUES (?, ?, ?, ?, ?, ?)',
                    (first_name, second_name, age, number, email, pswd))
                table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()['user_id']
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
    if request.method == 'POST':
        email = request.form['email']
        pswd = request.form['pswd']
        if not email or not pswd:
            flash('Пожалуйста, заполните формы', 'error')
        else:
            #session["name"] = first_name
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
            if not check_table_user_id:
                flash('Такая почта не найдена!', 'error')
                return redirect(url_for('authorization'))
            else:
                table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()['user_id']
                table_first_name = conn.execute('SELECT first_name FROM user where email = ?', (email,)).fetchone()['first_name']
                table_second_name = conn.execute('SELECT second_name FROM user where email = ?', (email,)).fetchone()['second_name']
                table_age = conn.execute('SELECT age FROM user where email = ?', (email,)).fetchone()['age']
                table_number = conn.execute('SELECT number FROM user where email = ?', (email,)).fetchone()['number']
                table_email = conn.execute('SELECT email FROM user where email = ?', (email,)).fetchone()['email']
                table_pswd = conn.execute('SELECT pswd FROM user where email = ?', (email,)).fetchone()['pswd']
                table_pic_name = conn.execute('SELECT pic_name FROM user where email = ?', (email,)).fetchone()['pic_name']
                #check = conn.execute('SELECT * FROM user where email = ?', (email,)).fetchone()['pswd']
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
                    session["pic_name"] = table_pic_name
                    session.permanent = True
                    return redirect(url_for('home'))
                else:
                    flash('Неверный пароль', 'error')
                    return redirect(url_for('authorization'))
    return render_template('authorization.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/restore_email", methods=('GET', 'POST'))
def restore_email():
    if request.method == 'POST':
        email = request.form['email']
        if not email:
            flash('Пожалуйста, заполните формы', 'error')
        else:
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
            if not check_table_user_id:
                flash('Такая почта не найдена!', 'error')
                return redirect(url_for('restore_email'))
            else:
                table_email = conn.execute('SELECT email FROM user where email = ?', (email,)).fetchone()['email']
                table_pswd = conn.execute('SELECT pswd FROM user where email = ?', (email,)).fetchone()['pswd']
                conn.close()
                x = random.randint(0,9999)
                message = "Код - " + str(x) #отправляется только английский текст...
                send_email(message, "Восстановление пароля", "longrast.2002@gmail.com", table_email) #message, subject, sender, recipient
                print("sent")
                session["email"] = table_email
                session["pswd"] = table_pswd
                session["x"] = x
                session.permanent = True
                return redirect(url_for('restore_password'))
    return render_template('restore-email.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/restore_password", methods=('GET', 'POST'))
def restore_password():
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
            message = "Код - " + str(x) #отправляется только английский текст...
            send_email(message, "Восстановление пароля", "longrast.2002@gmail.com", session["email"]) #message, subject, sender, recipient
            session["x"] = x
    return render_template('restore-password.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/contacts", methods=('GET', 'POST')) #добавить отправку
def contacts():
    if request.method == 'POST':
        name = request.form["first_name"]
        email = request.form['email']
        area = request.form['area']
        message = area
        send_email(message, f"Сообщение от пользователя: {name}", email, "longrast.2002@gmail.com") #message, subject, sender, recipient
        print(email)
        return redirect(url_for('contacts'))
    return render_template('contacts.html')

@app.route("/cosmetics-card")
def cosmetics_card():
    return render_template('cosmetics-card.html')

@app.route("/cosmetics")
def cosmetics():
    return render_template('cosmetics.html')

@app.route("/portfolio-card")
def portfolio_card():
    return render_template('portfolio-card.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/service_and_price")
def service_and_price():
    return render_template('service_and_price.html')


@app.route("/service_events")
def service_events():
    return render_template('service_events.html')

@app.route("/profile")
def profile():
    if session.get("user_id"):
        return render_template('profile.html')
    else:
        return abort(404)

@app.route("/profile_edit", methods=('GET', 'POST'))
def profile_edit():
    if session.get("user_id"):
        if request.method == 'POST':
            if session.get("_flashes"):
                session['_flashes'].clear()
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
                conn = get_db_connection()
                check_table_email = conn.execute('SELECT email FROM user where user_id = ?', (session["user_id"],)).fetchone()["email"]
                if email != check_table_email:
                    print("надо проверить")
                    check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
                    if check_table_user_id:
                        conn.close()
                        flash('Данная почта уже используется', 'error')
                        return redirect(url_for('profile_edit'))
                    else:

                        if profile_pic:
                            check_table_pic_name = conn.execute('SELECT pic_name FROM user where user_id = ?', (session["user_id"],)).fetchone()["pic_name"]
                            if check_table_pic_name != "unauthorized_user.png":
                                os.remove(f"static/images_users/{check_table_pic_name}")
                            print(check_table_pic_name)
                            pic_name = str(uuid.uuid1()) + os.path.splitext(profile_pic.filename)[1]
                            profile_pic.save(os.path.join("static/images_users", pic_name))
                        else:
                            pic_name = None

                        if profile_pic:
                            conn.execute('UPDATE user SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pswd = ?, pic_name = ? WHERE user_id = ?',
                                (first_name, second_name, age, number, email, pswd, pic_name, session["user_id"]))
                        else:
                            conn.execute('UPDATE user SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pswd = ? WHERE user_id = ?',
                                (first_name, second_name, age, number, email, pswd, pic_name, session["user_id"]))
                        conn.commit()
                        conn.close()
                        flash("Данные внесены", "noerror")
                        session["first_name"] = first_name
                        session["second_name"] = second_name
                        session["age"] = age
                        session["number"] = number
                        session["email"] = email
                        session["pswd"] = pswd
                        session["pic_name"] = pic_name
                        return redirect(url_for('profile'))
                else:

                    if profile_pic:
                        check_table_pic_name = conn.execute('SELECT pic_name FROM user where user_id = ?', (session["user_id"],)).fetchone()["pic_name"]
                        if check_table_pic_name != "unauthorized_user.png":
                            os.remove(f"static/images_users/{check_table_pic_name}")
                        print(check_table_pic_name)
                        pic_name = str(uuid.uuid1()) + os.path.splitext(profile_pic.filename)[1]
                        profile_pic.save(os.path.join("static/images_users", pic_name))
                    else:
                        pic_name = None

                    if profile_pic:
                        conn.execute('UPDATE user SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pswd = ?, pic_name = ? WHERE user_id = ?',
                            (first_name, second_name, age, number, email, pswd, pic_name, session["user_id"]))
                    else:
                        conn.execute('UPDATE user SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pswd = ? WHERE user_id = ?',
                            (first_name, second_name, age, number, email, pswd, pic_name, session["user_id"]))
                    conn.commit()
                    conn.close()
                    flash("Данные внесены", "noerror")
                    session["first_name"] = first_name
                    session["second_name"] = second_name
                    session["age"] = age
                    session["number"] = number
                    session["email"] = email
                    session["pswd"] = pswd
                    session["pic_name"] = pic_name
                    return redirect(url_for('profile'))
        return render_template('profile_edit.html')
    else:
        return abort(404)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/hello")
def hello():
    if "first_name" in session:
        temp = session["first_name"]
        content = "hello, " + temp
    else:
        content = "hello, stranger"
    return content


'''
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