from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from blog.model import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(
        message='Email is required field'), Email(message='Email not valid')])
    password = PasswordField('Password', validators=[
                             DataRequired(message='Password is required field')])
    remember_me = BooleanField(label="Remember me", default=True)
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email is required field'),
                                             Email(message='Email not valid'),
                                             Length(min=4, max=200, message='Email should be between 4-200 character long')])
    username = StringField('Username', validators=[DataRequired(message='Username is required field'),
                                                   Length(min=2, max=30, message='Username should be between 2-30 character long')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required field'),
                                                     EqualTo(
                                                         'pass_confirm', message='Passwords Must Match!'),
                                                     Length(min=6, max=200, message='Password should be between 6-200 characters long')])
    pass_confirm = PasswordField('Confirm password', validators=[
                                 DataRequired(message='Confirm Password is required field')])
    remember_me = BooleanField(label="Remember me", default=True)
    submit = SubmitField('Register!')

    def validate_email(self, email):
        # For verifying email is unique
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')

    def validate_username(self, username):
        # For verifying password is unique
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered')
        # For not allowing special character in username
        excluded_chars = " *?!'^+%&/()=}][{$#@"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(f'"{char}" is not allowed in username')


class ResetRequest(FlaskForm):
    email = StringField('Email', validators=[DataRequired(
        message='Email is required field'), Email(message='Email not valid')])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError(
                'Email not yet registered. Please register email first.')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message='Password is required field'),
                                                     EqualTo(
                                                         'pass_confirm', message='Passwords Must Match!'),
                                                     Length(min=6, max=200, message='Password should be between 6-200 characters long')])
    pass_confirm = PasswordField('Confirm password', validators=[
                                 DataRequired(message='Confirm Password is required field')])
    submit = SubmitField('Reset Password')


class OTPForm(FlaskForm):
    otp = StringField(label='OTP', validators=[
                      DataRequired(), Length(min=6, max=6, message='Invalid OTP')])
    submit = SubmitField('Register')
