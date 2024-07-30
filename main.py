from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from libgravatar import Gravatar
from functools import wraps
from random import randint
from mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# LOGIN MANAGER STUFF
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "blog-users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(1000))
    gravatar = db.Column(db.String(1000))

    # One-to-Many relationship with Blogpost() - Parent.
    post = db.relationship('BlogPost', back_populates='user')

    # One-to-Many relationship with Comment() - Parent.
    user_comment = db.relationship('Comment', back_populates='user')


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # One-to-Many relationship with User() - Child
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    user_id = db.Column(db.Integer, db.ForeignKey('blog-users.id'))
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    user = db.relationship("User", back_populates="post")

    # One-to-Many relationship with Comment() - Parent.
    post_comment = db.relationship('Comment', back_populates='post')


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # One-to-Many relationship with User() - Child
    user_id = db.Column(db.Integer, db.ForeignKey('blog-users.id'))
    user = db.relationship("User", back_populates="user_comment")

    # One-to-Many relationship with Blogpost() - Child
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    post = db.relationship("BlogPost", back_populates="post_comment")


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(404)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    my_form = RegisterForm()
    if my_form.validate_on_submit():
        user = User()
        user.email = my_form.email.data.lower()
        user.name = my_form.username.data.title()
        user.gravatar = Gravatar(my_form.email.data.lower()).get_image(size=520, default='robohash')

        password = my_form.password.data

        if user.query.filter_by(email=user.email).first() or user.query.filter_by(name=user.name.title()).first():
            flash(f"Username or Email address already exists!", 'info')
            return redirect(url_for('register'))

        salt_length = randint(16, 32)
        user.password = generate_password_hash(
            password,
            method='pbkdf2:sha3_512:100000',
            salt_length=salt_length
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=my_form, current_user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data.title()).first()
        if user is None:
            user = User.query.filter_by(email=form.name.data.lower()).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("No user found with that username, or password invalid.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)

    if not requested_post:
        return abort(404)

    my_form = CommentForm()
    if my_form.validate_on_submit():
        new_comment = Comment(
            text=my_form.comment_text.data,
            user=current_user,
            post=requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('show_post', post_id=post_id))

    return render_template("post.html", post=requested_post, form=my_form, current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm(author=current_user.name)
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y"),
            user=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
        )
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.subtitle = edit_form.subtitle.data
            post.img_url = edit_form.img_url.data
            post.author = edit_form.author.data
            post.body = edit_form.body.data
            db.session.commit()
            return redirect(url_for("show_post", post_id=post.id))

        return render_template("make-post.html", form=edit_form, current_user=current_user)

    return abort(404)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts', current_user=current_user))


@app.route("/delete-comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    if comment_to_delete:
        if current_user.id == comment_to_delete.user.id or current_user.id == 1:
            post_id = comment_to_delete.post.id
            db.session.delete(comment_to_delete)
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id, current_user=current_user))

    return abort(404)


@app.route("/edit-comment/<int:comment_id>", methods=['POST', 'GET'])
@login_required
def edit_comment(comment_id):
    comment_to_edit = Comment.query.get(comment_id)
    if comment_to_edit:
        my_form = CommentForm(comment_text=comment_to_edit.text)
        if my_form.validate_on_submit():
            comment_to_edit.text = my_form.comment_text.data
            db.session.commit()
            post_id = comment_to_edit.post.id
            return redirect(url_for("show_post", post_id=post_id, form=my_form))
        return render_template("post.html", post=comment_to_edit.post, form=my_form, current_user=current_user)

    return abort(404)


@app.route("/contact", methods=["POST", "GET"])
def receive_data():
    if request.method == 'POST':
        data = request.form
        Mail(data)
        return render_template("contact.html", success='Successfully sent your message.')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
