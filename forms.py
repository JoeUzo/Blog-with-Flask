from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={"placeholder": "Retype Password"})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username or Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class CommentForm(FlaskForm):
    comment_text = TextAreaField("Add a Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
