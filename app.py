import sqlite3
from flask import *
#Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import *
#abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

#import re
#from datetime import datetime

#from flask import send_from_directory
#from flask import Flask, render_template

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/authorization")
def authorization():
    return render_template('authorization.html')

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

@app.route("/registration", methods=('GET', 'POST'))
def registration():
    flash('Ок')
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        age = request.form['age']
        email = request.form['email']
        pswd = request.form['pswd']
        if not email or not pswd:
            flash('Пожалуйста, заполните формы')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO user (first_name, second_name, age, email, pswd) VALUES (?, ?, ?, ?, ?)',
                         (first_name, second_name, age, email, pswd))
            conn.commit()
            conn.close()
            return redirect(url_for('registration'))
    return render_template('registration.html')

@app.route("/restore_password")
def restore_password():
    return render_template('restore-password.html')

@app.route("/service_and_price")
def service_and_price():
    return render_template('service_and_price.html')


@app.route("/service_events")
def service_events():
    return render_template('service_events.html')

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