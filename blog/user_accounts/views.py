from flask import Blueprint,render_template,redirect,url_for,flash,request
from blog.model import User
from blog import db,app
from blog.user_accounts.forms import RegistrationForm,LoginForm,ResetRequest,ResetPassword, OTPForm
from flask_login import login_user,login_required,logout_user, current_user
from werkzeug.security import generate_password_hash
from blog.user_accounts.email_validation import send_reset_email,send_verification_email

user_account_blueprint = Blueprint('user_accounts',
                                    __name__,)
@user_account_blueprint.route('/register/',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        username = form.username.data
        user = User(username,password,email)
        otp = send_verification_email(user) 
        token = user.get_verification_token(otp = otp)    
        return redirect(url_for('user_accounts.otp_verification',token=token,remember_me=form.remember_me.data))

    return render_template('user_accounts/register.html',form=form)
@user_account_blueprint.route('/verify_email/<token>', methods=['GET','POST'])
def otp_verification(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Token Processing
    user,otp = User.verify_verification_token(token)
    remember_me = request.args.get('remember_me')
    remember_me = True if remember_me == 'True' else False
    if user is None or otp is None:
        flash('Invalid or expired token')
        return redirect(url_for('user_accounts.login'))
    
    # Validate OTP
    form = OTPForm()
    if form.validate_on_submit():
        if not form.otp.data == str(otp):
            flash('Invalid OTP')
            return redirect(url_for('user_accounts.otp_verification',token=token))
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=remember_me)
        return redirect(url_for('home'))
    return render_template('user_accounts/otp_verification.html',form=form)
@user_account_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_accounts.login'))

@user_account_blueprint.route('/login/',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user,remember=form.remember_me.data)
            next_ = request.args.get('next')
            if next_ == None or not next_[0]=='/':
                next_ = url_for('home')

            return redirect(next_)
        else:
            flash("Incorrect email or password",'danger')
    return render_template('user_accounts/login.html',form=form)







@user_account_blueprint.route('reset_password',methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Password reset link has been sent to the provided email.','info')
        return redirect(url_for('user_accounts.login'))
    return render_template('user_accounts/reset_request.html',form=form)

@user_account_blueprint.route('reset_password/<token>',methods = ['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash('The token was invalid or experied.')
        return redirect(url_for('user_accounts.login'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Password reset successful! You could login now.','info')
        return redirect(url_for('user_accounts.login'))
    return render_template('user_accounts/reset_password.html',form=form)