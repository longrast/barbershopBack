import sqlite3
import random
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from datetime import timedelta
from flask_mail import Mail, Message #говно не работает
import smtplib

import re
import smtplib
import dns.resolver
import socket
'''
import re; 
from dns import resolver; 
import socket; import smtplib;
'''


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
'''
def check_email_if_exists(email):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.connect()
    server.set_debuglevel(True)
    try:
        server.verify(email)
        print("try")
    except Exception:
        print("bad")
        return False
    finally:
        print("end")
        server.quit()
'''

def send_email(message):
    sender = "longrast.2002@gmail.com"
    # your password = "your password"
    password = "xldqywyphzrjbafr"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        print("sent1")
        server.sendmail(sender, sender, message) #sender, recipient, msg
        print("sent2")
        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")

        return True
    except Exception as _ex:
        print("sent3")
        return False

def check_if_email_exists(email):
    email_address = email

    #Step 1: Check email
    #Check using Regex that an email meets minimum requirements, throw an error if not
    addressToVerify = email_address
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
        flash('Возможно, вы неправильно ввели адрес ')
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
    '''
    x = 1
    msg = Message('Hello', sender= "noreply@app.com", recipients = [app.config['MAIL_USERNAME']])
    msg.body = ("Your code is ?", (x))
    mail.send(msg)
    '''
    #send_email("ok")
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
        if not email or not pswd:
            flash('Пожалуйста, заполните формы')
        elif not check_if_email_exists(email):
            flash('Такой почты не существует')
        else:
            #session["name"] = first_name
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
            if check_table_user_id:
                conn.close()
                flash('Вы уже зарегистрированы!')
                return redirect(url_for('authorization'))
            conn.execute('INSERT INTO user (first_name, second_name, age, number, email, pswd) VALUES (?, ?, ?, ?, ?, ?)',
                (first_name, second_name, age, number, email, pswd))
            table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()['user_id']
            conn.execute("INSERT INTO access (access_id, role) VALUES (?, ?)",
                (table_user_id, '2'))
            conn.commit()
            conn.close()
            return redirect(url_for('authorization'))
    return render_template('registration.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/authorization", methods=('GET', 'POST'))
def authorization():
    if request.method == 'POST':
        email = request.form['email']
        pswd = request.form['pswd']
        if not email or not pswd:
            flash('Пожалуйста, заполните формы')
        else:
            #session["name"] = first_name
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
            if not check_table_user_id:
                flash('Такая почта не найдена!')
                return redirect(url_for('authorization'))
            else:
                table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()['user_id']
                table_first_name = conn.execute('SELECT first_name FROM user where email = ?', (email,)).fetchone()['first_name']
                table_second_name = conn.execute('SELECT second_name FROM user where email = ?', (email,)).fetchone()['second_name']
                table_age = conn.execute('SELECT age FROM user where email = ?', (email,)).fetchone()['age']
                table_number = conn.execute('SELECT number FROM user where email = ?', (email,)).fetchone()['number']
                table_email = conn.execute('SELECT email FROM user where email = ?', (email,)).fetchone()['email']
                table_pswd = conn.execute('SELECT pswd FROM user where email = ?', (email,)).fetchone()['pswd']
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
                    session.permanent = True
                else:
                    flash('Неверный пароль')
                return redirect(url_for('home'))
    return render_template('authorization.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/restore_email", methods=('GET', 'POST'))
def restore_email():
    if request.method == 'POST':
        email = request.form['email']
        if not email:
            flash('Пожалуйста, заполните формы')
        else:
            conn = get_db_connection()
            check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
            if not check_table_user_id:
                flash('Такая почта не найдена!')
                return redirect(url_for('restore_email'))
            else:
                table_email = conn.execute('SELECT email FROM user where email = ?', (email,)).fetchone()['email']
                table_pswd = conn.execute('SELECT pswd FROM user where email = ?', (email,)).fetchone()['pswd']
                conn.close()
                x = random.randint(0,9999)
                message = "Your code is " + str(x) #отправляется только английский текст...
                send_email(message)
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
    flash("Код был выслан на почту")
    if request.method == 'POST':
        session['_flashes'].clear()
        code = request.form['code']
        if str(code) == str(session["x"]):
            flash("Ваш пароль отправлен на почту")
            password = str(session["pswd"])
            message = "Your password is " + password #отправляется только английский текст...
            send_email(message)
        else:
            flash("Ваш код неправильный, проверьте почту еще раз")
            x = random.randint(0,9999)
            message = "Your code is " + str(x)
            send_email(message)
            session["x"] = x
    return render_template('restore-password.html')

#-------------------------------------------------------------------------------------------------------------

@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/contacts")
def contacts():
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
            if not email or not pswd:
                flash('Пожалуйста, заполните формы')
            else:
                conn = get_db_connection()
                check_table_email = conn.execute('SELECT email FROM user where user_id = ?', (session["user_id"],)).fetchone()["email"]
                if email != check_table_email:
                    print("надо проверить")
                    check_table_user_id = conn.execute('SELECT user_id FROM user where email = ?', (email,)).fetchone()
                    if check_table_user_id:
                        conn.close()
                        flash('Данная почта уже используется')
                        return redirect(url_for('profile_edit'))
                    else:
                        conn.execute('UPDATE user SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pswd = ? WHERE user_id = ?',
                            (first_name, second_name, age, number, email, pswd, session["user_id"]))
                        conn.commit()
                        conn.close()
                        flash("Данные внесены")
                        session["first_name"] = first_name
                        session["second_name"] = second_name
                        session["age"] = age
                        session["number"] = number
                        session["email"] = email
                        session["pswd"] = pswd
                        return redirect(url_for('profile'))
                else:
                    conn.execute('UPDATE user SET first_name = ?, second_name = ?, age = ?, number = ?, email = ?, pswd = ? WHERE user_id = ?',
                        (first_name, second_name, age, number, email, pswd, session["user_id"]))
                    conn.commit()
                    conn.close()
                    flash("Данные внесены")
                    session["first_name"] = first_name
                    session["second_name"] = second_name
                    session["age"] = age
                    session["number"] = number
                    session["email"] = email
                    session["pswd"] = pswd
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