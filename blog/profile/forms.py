from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,Length
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from blog.model import User
from flask_login import current_user
from werkzeug.security import check_password_hash
class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required field'),
                                                    Length(min=2,max=30,message='Username should be between 2-30 character long')])
    
    profile_pic = FileField('Profile Pic',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update!')
   
    def validate_username(self, username):
        # For verifying password is unique
        if current_user.username != self.username.data:
            if User.query.filter_by(username=self.username.data).first():
                raise ValidationError('Username has been registered')

class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password',validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(message='Password is required field'), 
                                                    Length(min=6,max=200,message='Password should be between 6-200 characters long')])
    submit = SubmitField('Change Password')
    def validate_old_password(self,old_password):
        if not check_password_hash(current_user.password,self.old_password.data):
            raise ValidationError('The password is invalid.')