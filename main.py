from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import pandas as pd
from werkzeug.utils import secure_filename
import os

db=SQLAlchemy()
DB_NAME= 'database.db'
app = Flask(__name__)
app.config['SECRET_KEY']='bene'
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


adminkey='z'

username=''

def create_database(app):
    db.init_app(app)
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database creaated")
        
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,unique=True)
    fullName=db.Column(db.String(100))
    password=db.Column(db.String(100))  
    
    
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
def home():
  return render_template('index.html')

@app.route("/dash")
def dash():
  return render_template('dash.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/contact")
def contact():
  return render_template('contact.html')



@app.route("/logins")
def logins():
  return render_template('logins.html')

@app.route("/logint", methods=['GET', 'POST'])
def logint():
  if request.method == 'POST':
    username= request.form['email']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
          login_user(user, remember=True)
          return redirect('/dash')
        else:
          print('Wrong pass')
  return render_template('logint.html')

@app.route("/register", methods=["POST", "GET"])
def register():
  if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email   = request.form['email']
        adminkey = request.form['adminkey']
        if adminkey != 'aisat123':
            return redirect(url_for('logint'))   
        new_user=User(fullName=username,password=password,email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('logint'))

  else:
      return render_template('register.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
        # Access the uploaded file
        file = request.files['csv_file']

       

        # Save the file to the static/files folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file (e.g., read and manipulate the CSV data)
        df = pd.read_csv(file_path)
        print(df)
        # Your processing logic goes here

        return "File uploaded and processed successfully!"
  return render_template('upload.html')








@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))

# main driver function
if __name__ == '__main__':
    create_database(app)
    app.run(host="0.0.0.0", debug=True)