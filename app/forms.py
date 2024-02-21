from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from app.routes import Session


class RegistrationForm(FlaskForm):
    user_name = StringField('user name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField("remember me", default=False)
    
    submit = SubmitField("Sign up")

    '''def validate_email(form, email):
        sess = Session()
        user = sess.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one")'''
            


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sign in')
