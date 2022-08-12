from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt
from random import randint
from secret import *
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate

phi_of_n = (p-1)*(q-1)
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

#SQLite DB used locally
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#first_postgres
#app.config['SQLALCHEMY_DATABASE_URI'] = ''

#second_postgres
#app.config['SQLALCHEMY_DATABASE_URI'] = ''

#third_postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tdvoazvckmsvzl:b18947eaaf52c69a2b3bf56d7e0cd253de44ac7f390a0390a945acd89effb2cd@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dfsgpr5f7ea43o'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'secretkey'
bcrypt = Bcrypt(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(500), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    content = db.Column(db.String(500))
    public_key = db.Column(db.Integer)
    one_time_login = db.Column(db.Integer, nullable = False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forgot')
def forgot():
    return 'YOOOOO \n \t say sike'

def validate_login(username):
    existing_username = User.query.filter_by(username = username).first()
    if existing_username:
        return True
    else:
        return False
        #raise ValidationError("No such username exists. Please register first.")

@app.route('/login', methods= ["GET", "POST"])
def login():
    if request.method == "POST":
        input_username = request.form["logname"]
        input_password = request.form["logpass"]
        if validate_login(input_username):
            user = User.query.filter_by(username = input_username).first()
            if bcrypt.check_password_hash(user.password, input_password):
                login_user(user)
                return dashboard(input_username, input_password)
            else:
                flash("Username and Password do not match.")
                return render_template('index.html')
                #raise ValidationError("Username and Password do not match.")
        else:
            flash("No such username exists. Please register first.")
            return render_template('index.html')
            
@app.route('/dashboard', methods = ["GET", "POST"])
@login_required
def dashboard(input_username, input_password):
    return render_template('ask_for_private_key.html', username = input_username)

def encrypt(message, e):
    res = ''.join(format(ord(i), '08b') for i in message)
    int_res = int(res, 2)
    encrypted_res = pow(int_res, e, n)
    return encrypted_res

def decrypt(num, d):
    ans = []
    decrypted_val = pow(num, d, n)
    decrypted_val_binary = bin(decrypted_val)[2:]
    if len(decrypted_val_binary) == 0:
        return "Your text here."
    ascii_val = int(decrypted_val_binary[:len(decrypted_val_binary)%8], 2)
    ans.append(chr(ascii_val))
    for i in range(len(decrypted_val_binary)%8, len(decrypted_val_binary), 8):
        ascii_val = int(decrypted_val_binary[i:i+8], 2)
        ans.append(chr(ascii_val))
    return ''.join(ans)

def validate_private_key(priv_key, public_key):
    if (priv_key*public_key) % phi_of_n == 1:
        return True
    else:
        return False

@app.route('/content', methods = ["GET", "POST"])
@login_required
def content():
    if request.method == "POST":
        private_key = request.form["priv_key"]
        username = request.form["username"]
        private_key = int(private_key)
        user = User.query.filter_by(username = username).first()
        if validate_private_key(private_key, user.public_key):
            if user.content == None or user.content == "":
                current_content = "Your text here."
            else:
                current_content = decrypt(int(user.content), private_key)
            return render_template('display.html', current_content = current_content, username = username)
        else:
            logout_user()
            flash("Incorrect Private Key. You have been logged out.")
            return render_template('index.html')

@app.route('/content_two', methods = ["GET", "POST"])
@login_required
def content_two():
    if request.method == "POST":
        username = request.form["username"]
        data = request.form["message"]
        user = User.query.filter_by(username = username).first()
        if data == "" or data == None:
            user.content = None
            db.session.commit()
            current_content = "Your text here."
            return render_template('display.html', current_content = current_content, username = username)
        else:
            content = encrypt(data, user.public_key)
            user.content = str(content)
            db.session.commit()
            return render_template('display.html', current_content = data, username = username)

@app.route('/logout', methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def validate_user(username, email):
    existing_username = User.query.filter_by(username = username).first()
    if existing_username:
        return 1
        #raise ValidationError("The username already exists. Please chose another username.")
    existing_email = User.query.filter_by(email = email).first()
    if existing_email:
        return 2
        #raise ValidationError("The email is already used. Please chose another email.")
    return True

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        return 0
    else:
        MI = (x_old + MOD) % MOD
        return MI

def create_keys():
    '''
    creates d and e for the user
    return (d, e)
    '''
    arr = ['-1' for j in range(12)]
    while True:
        arr[-1] = '1'
        for i in range(11):
            arr[i] = str(randint(0, 1))
        final = int(''.join(arr), 2)
        check = MI(final, phi_of_n)
        if check > 0 and final > 0:
            existing_e = User.query.filter_by(public_key = final).first()
            if not existing_e:
                return (check, final)

@app.route('/register', methods= ["GET", "POST"])
def register():
    if request.method == "POST":
        input_username = request.form["logname"]
        input_email = request.form["logemail"]
        input_password = request.form["logpass"]
        value = validate_user(input_username, input_email)
        if value == True:
            d, e = create_keys()
            hashed_password = bcrypt.generate_password_hash(input_password).decode('utf-8')
            new_user = User(username = input_username, password = hashed_password, email = input_email, one_time_login = 0, public_key = e)
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(username = input_username).first()
            login_user(user)
            return render_template('first_time.html', private_key = d)
        elif value == 1:
            flash("The username already exists. Please chose another username.")
            return render_template('index.html')
        elif value == 2:
            flash("The email is already used. Please chose another email.")
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)