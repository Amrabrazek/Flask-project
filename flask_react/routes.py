from flask import render_template, redirect, url_for, flash
from flask_react import app
from flask_react.forms import RegistrationForm, LoginForm


Navbar = ['home', 'about', 'login']

@app.route('/home')
@app.route('/')
def home():
    endpoint_title = 'home'
    return render_template('home.html', data={ 'title':endpoint_title, 'Navbar':Navbar})

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("Login Successful", "success")
        return redirect(url_for('home'))

    endpoint_title = 'login'
    return render_template('login.html', data={'title':endpoint_title, 'Navbar':Navbar, 'form':form})

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash("Registered Successful", "success")
        return redirect(url_for('login'))

    endpoint_title = 'login'
    return render_template('register.html', data={'title':endpoint_title, 'Navbar':Navbar, 'form':form})



if __name__ == '__main__':
    app.run(debug=True)

