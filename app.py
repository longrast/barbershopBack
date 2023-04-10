import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from datetime import timedelta

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = 'verystrongsecretkey'
app.permanent_session_lifetime = timedelta(minutes=2)

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
        if not email or not pswd:
            flash('Пожалуйста, заполните формы')
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

@app.route("/restore_password")
def restore_password():
    return render_template('restore-password.html')

@app.route("/service_and_price")
def service_and_price():
    return render_template('service_and_price.html')


@app.route("/service_events")
def service_events():
    return render_template('service_events.html')

@app.route("/profile")
def profile():
    if session:
        return render_template('profile.html')
    else:
        return abort(404)

@app.route("/profile_edit")
def profile_edit():
    if session:
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