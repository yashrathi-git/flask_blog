from flask_mail import Message
from blog import mail
from flask import url_for
from random import randint
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Link', sender='noreply@localhost.com', recipients=[user.email])
    msg.body = f"""To reset password click the following link:-
{url_for('user_accounts.reset_password',token=token, _external=True)}
If you didn't made this request just ignore this email.
The link is only valid for 30 minutes.
    """
    mail.send(msg)

def send_verification_email(user):
    msg = Message(subject='Email Verification', sender='noreply@localhost.com', recipients=[user.email])
    otp = randint(100000,999999)
    msg.body = f"""Please register with the following otp :-
{otp}
    """
    mail.send(msg)
    return otp