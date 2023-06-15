from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_react import  app, bcrypt, db
from flask_react.models import User, Post
from flask_react.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os 
from datetime import datetime


users = Blueprint(
    'users',
    __name__,
    url_prefix = '/users'
)

Navbar = ['home', 'profile', "friends" , 'logout']

@app.route('/home')
@app.route('/')
@login_required
def home():
    endpoint_title = 'home'
    return render_template('home.html', data={ 'title':endpoint_title, 'Navbar':Navbar})

@app.route('/about')
@login_required
def about():
    endpoint_title = 'about'
    return render_template('about.html', data={ 'title':endpoint_title, 'Navbar':Navbar})



@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        
        with app.app_context():
            # birth_date = form.date.data
            # birth_date = birth_date.date()
            image_bytes = form.image.data.read()
            hashed_pw = bcrypt.generate_password_hash(form.password.data)
            new_user = User(middle_name=form.middle_name.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            username=form.username.data,
                            birth_date=form.date.data,
                            image=image_bytes,
                            email=form.email.data,
                            password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

        file = form.image.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        # return "File has been uploaded."

        flash("Registered Successful", "success")
        return redirect(url_for('login'))
    
    endpoint_title = 'login'
    return render_template('register.html', data={'title':endpoint_title, 'Navbar':Navbar, 'form':form})


@app.route('/login', methods = ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    endpoint_title = 'login'
    if form.validate_on_submit():
        with app.app_context():
            user=User.query.filter_by(
                email = form.email.data
                ).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login Successful", "success")
                next_page = request.args.get('next')
                if next_page :
                    return redirect(next_page)
                else :
                    return redirect(url_for('home'))
            else:
                flash("Login unSuccessful", "danger")
                return redirect(url_for('login'))
            
    return render_template('login.html', data={'title':endpoint_title, 'Navbar':Navbar, 'form':form})

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
        image = current_user.image.decode('utf-8')
        endpoint_title = 'profile'
        return render_template('profile.html', data={ 'title':endpoint_title, 'Navbar':Navbar, 'user':current_user, 'image':image })

@app.route('/friends')
@login_required
def friends():
        endpoint_title = 'friends'
        return render_template('friends.html', data={ 'title':endpoint_title, 'Navbar':Navbar})

if __name__ == '__main__':
    app.run(debug=True)

