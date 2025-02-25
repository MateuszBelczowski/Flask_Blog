
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
import flask_whooshalchemyplus
from flaskblog.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required




# posts = [
#     {
#         'author': 'Joseph Sowah',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'July 19, 2019'
    
#     }, 

#     {

#         'author': 'John Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'July 20, 2019'
    
#     }
# ]


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route('/search')
def search():
    q = request.args.get('q')
    posts = Post.query.z(q).all()
    return render_template('home.html', posts=posts)  

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(email=form.email.data)
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#   in python if you want to throw 
# away a variable or you won't use the variable, 
# you need to use the underscore
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/avatar', picture_fn)
    img = Image.open(form_picture)
    img.thumbnail((125, 125))
    img.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
         
    image_file = url_for('static', filename='avatar/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    flash("Your post has been successfully deleted", "success")
    return redirect(url_for('home'))

    
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)




     
















    
    # About 46% of contributors on tensorflow are based in africa
    # Google -  Research
    # How machine Learning can help break language barrier in Africa.. Africa is  about 2.4Billion
    # Census is really expensive some of the time the statics are outdated.
    # Analysis of satellite images
    # Ai enabled flood forcasting. The app sends a notification whenever there's a chance of flood occurrence


    # Daibetic retinopathy fastest growing cause of blindess in the continent
    # Regular screening is key to prevention about 45% suffer vision loss before diagnosis
    # Deep learning can help analysis images to help i dentify whether a person have diabetic retinopathy



# Statistica



# Web VR....is an open source web platform where you can expirement with VR. you can code webVR with 
# HTMl 
# Issues in VR Ecosystem
# Gatekeepers
# installs
# closed
#   wrting VR code is complex so mozilla introduced A-frame to help minimze the codes we need to write






  


