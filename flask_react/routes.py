from flask import render_template, redirect, url_for, flash
from flask_react import app
from flask_react.forms import RegistrationForm, LoginForm


Navbar = ['home', 'about']

@app.route('/home')
@app.route('/')
def home():
    endpoint_title = 'home'
    return render_template('home.html', data={ 'title':endpoint_title, 'Navbar':Navbar})

