from flask import render_template, redirect, url_for, flash, request, Blueprint, send_from_directory
from flask_react import  app, bcrypt, db
from flask_react.models import User, Post, Friendship
from flask_react.forms import RegistrationForm, LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os 
from datetime import datetime, date
from PIL import Image
import io
import base64

from flask_uploads import UploadSet, IMAGES, configure_uploads



users = Blueprint(
    'users',
    __name__,
    url_prefix = '/users'
)

Navbar = ['home', 'profile', "friends" , 'logout']

@app.route('/home', methods = ['GET', 'POST'])
@app.route('/', methods = ['GET', 'POST'])
@login_required
def home():

    form = PostForm()

    if form.validate_on_submit():
        
        with app.app_context():
            new_post = Post(title=form.title.data,
                            content=form.content.data,
                            status=form.status.data,
                            user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()

        flash("Post added Successful", "success")
        return redirect(url_for('home'))
    
    friend_posts = []
    friendships = Friendship.query.filter((Friendship.user_id == current_user.id)).all()
    for friendship in friendships:
        # friend_id = friendship.friend_id if friendship.user_id == user_id else friendship.user_id
        friend_posts += User.query.get(friendship.friend_id).posts

    print('00000000000000000000000000000000000')

    friends_posts  = list(filter(lambda post : post.status == 'Friends_only' , friend_posts ))
    
    posts_id = []

    for post in friends_posts:
        posts_id.append(post.id)

    print(posts_id)
    print(friends_posts)
    # for post in friend_posts:
    #     print(post.status)
    # print(friend_posts)

    posts_onlyme = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter(Post.user_id == current_user.id)\
        .order_by(Post.date.desc())\
        .all()
    
    # print('--------------------------------')
    # print(posts_onlyme)
    # posts_friends = db.session.query(
    #     Post,

    friendsandI_posts = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter(Post.id.in_(posts_id))\
        .order_by(Post.date.desc())\
        .all()
    
    print('--------------------------------')
    for post in friendsandI_posts:
        print(post.Post.id)
    # print(friendsandI_posts[2].user_id)

    posts_public = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter((Post.status == "Public") | (Post.user_id == current_user.id) | (Post in friends_posts))\
        .order_by(Post.date.desc())\
        .all()

    endpoint_title = 'home'
    return render_template('home.html', data={ 'title':endpoint_title, 'Navbar':Navbar, 'form': form, "posts_onlyme": posts_onlyme, "posts_public":posts_public, "friends_only_posts":friendsandI_posts })

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
            # print(form.image.data)
            profile_image = form.profile_image.data
            hashed_pw = bcrypt.generate_password_hash(form.password.data)
            new_user = User(middle_name=form.middle_name.data.capitalize(),
                            first_name=form.first_name.data.capitalize(),
                            last_name=form.last_name.data.capitalize(),
                            username=form.username.data,
                            birth_date=form.date.data,

                            # image=image_bytes,
                            profile_image_data = profile_image.read(),
                            profile_image_filename = profile_image.filename,

                            email=form.email.data,
                            password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

        # UPLOADING IMAGE TO STATIC/PROFILE_IMAGES


        file = form.profile_image.data # First grab the file
        filename = secure_filename(file.filename)
        file.seek(0)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)) # Then save the file
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # profile_image = request.files['profile_image']
        # filename = secure_filename(profile_image.filename)
        # profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # return "File has been uploaded."

        # photos = UploadSet("profile_image", IMAGES)
        # configure_uploads(app, photos)

        # filename = photos.save(form.profile_image.data)
        # file_url = url_for('get_file', filename=filename)

        # pic = form.profile_image.data
        # pic_name = secure_filename(pic.filename)
        # print(pic_name)
        # pic_type = pic.mimetype
        # print(pic_type)

        flash("Registered Successful", "success")
        return redirect(url_for('login'))
    
    endpoint_title = 'login'
    return render_template('register.html', data={'title':endpoint_title, 'Navbar':Navbar, 'form':form})


# @app.route('/uploads/<filename>')
# def get_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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

# @app.route('/display/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='profile_images/' + filename), code=301)


@app.route('/profile')
@login_required
def profile():
        # image = current_user.image.decode('utf-8')
        # print(current_user.image)
        today = date.today()
        born = current_user.birth_date
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        endpoint_title = 'profile'


        # image = Image.open(io.BytesIO(current_user.profile_image_data))

        # buffered = io.BytesIO()
        # image.save(buffered, format="JPEG")
        # img_str = base64.b64encode(buffered.getvalue()).decode()


        return render_template('profile.html', data={ 'title':endpoint_title, 'Navbar':Navbar, 'user':current_user, 'age': age  })

@app.route('/friends')
@login_required
def friends():
        endpoint_title = 'friends'
        return render_template('friends.html', data={ 'title':endpoint_title, 'Navbar':Navbar})

if __name__ == '__main__':
    app.run(debug=True)

