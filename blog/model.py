from blog import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, unique = True, nullable=False)
    password = db.Column(db.String, nullable= False)
    email = db.Column(db.String, nullable= False)
    image_file = db.Column(db.String, nullable = False, default = 'default.jpg')
    post = db.relationship('Post',backref='author',lazy=True)
    def __init__(self,username,password,email,hash_=True):
        """
        INPUT
        username, unhashed password, email,hash_
        """
        self.username = username
        self.password = generate_password_hash(password) if hash_ else password
        self.email = email

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def get_verification_token(self,otp,expiration_time=900):
        s = Serializer(app.config['SECRET_KEY'],expiration_time)
        return s.dumps({'username':self.username,'email':self.email,'password':self.password, 'otp':otp}).decode('utf-8')
    @staticmethod
    def verify_verification_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_info = s.loads(token)
            username = User.query.filter_by(username = user_info['username']).first()
            email = User.query.filter_by(email = user_info['email']).first()
            if username or email:
                raise Exception('Username or email already exists.')
        except:
            return None,None
        return User(username=user_info['username'],
                email=user_info['email'],
                password=user_info['password'],
                hash_ = False,),user_info['otp']
            

    def get_reset_token(self,expiration_time=1800):
        s = Serializer(app.config['SECRET_KEY'],expiration_time)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return 
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = False)
    title = db.Column(db.String(128), nullable = False)
    short_description = db.Column(db.String(250), nullable=False)
    post = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime)
    
    def __init__(self,user_id,title,post,short_description):
        self.user_id = user_id
        self.post = post
        self.title = title
        self.date = datetime.now()
        self.short_description = short_description