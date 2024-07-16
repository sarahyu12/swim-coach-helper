import os, random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import pymongo
from models import User
import csv
from datetime import date
import hashlib


app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECRET_KEY'] = os.environ['SUPERSECRETKEY']
client = pymongo.MongoClient(os.environ['DATABASE_URI'])
db = client.get_database('swimmers')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User()


@app.route('/')  # What happens when the user visits the site
def home():
    return render_template('base.html', user=current_user)

@app.route('/login')
def login():
    return render_template('login.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html', user=current_user)


@app.route('/login', methods=['POST'])
def login_post():
    user = User()
    username = request.form.get('username')
    password = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
    if user.get_username != username or user.get_password != password:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    else:
        login_user(user)
    return redirect(url_for('success'))


@app.route('/success')
@login_required
def success():
    return render_template('base.html', user=current_user)

@app.route('/timer', methods=['GET'])
@login_required
def timer_page():
  if request.method == "GET":
    name_list = []
    with open('names.csv') as csvfile:    
	    csvReader = csv.reader(csvfile)    
	    for row in csvReader:        
		    name_list.append(row[0])   
    return render_template('timer.html',user=current_user, name_list=name_list)
    
@app.route('/timer', methods=['POST'])
def timer_post():
  nameSwimmer1 = request.form.get('nameSwimmer1')
  nameSwimmer2 = request.form.get('nameSwimmer2')
  nameSwimmer3 = request.form.get('nameSwimmer3')
  millisTimer1 = request.form.get('millisTimer1') #these are actually seconds 
  millisTimer2 = request.form.get('millisTimer2')
  millisTimer3 = request.form.get('millisTimer3')
  strokeSwimmer1 = request.form.get('strokeSwimmer1')
  strokeSwimmer2 = request.form.get('strokeSwimmer2')
  strokeSwimmer3 = request.form.get('strokeSwimmer3')
  distanceSwimmer1 = request.form.get('distanceSwimmer1')
  distanceSwimmer2 = request.form.get('distanceSwimmer2')
  distanceSwimmer3 = request.form.get('distanceSwimmer3')
  if nameSwimmer1 != "" and millisTimer1 != "":
    age_group = ""
    gender = ""
    with open('names.csv') as csvfile:
      csvReader = csv.reader(csvfile)
      for row in csvReader:
        if row[0] == nameSwimmer1:
          age = int(row[2])
          age_group = getAgeGroup(age)
          gender = row[1]
          mydict = { "name": nameSwimmer1, "gender": gender, "age_group": age_group, "stroke": strokeSwimmer1, "distance": distanceSwimmer1, "time": float(millisTimer1), "date": date.today().isoformat()}
          db.times.insert_one(mydict)
          

  if nameSwimmer2 != "" and millisTimer2 != "":
    age_group = ""
    gender = ""
    with open('names.csv') as csvfile:
      csvReader = csv.reader(csvfile)
      for row in csvReader:
        if row[0] == nameSwimmer2 and millisTimer2 != "":
          age = int(row[2])
          age_group = getAgeGroup(age)
          gender = row[1]
          mydict = { "name": nameSwimmer2, "gender": gender, "age_group": age_group, "stroke": strokeSwimmer2, "distance": distanceSwimmer2, "time": float(millisTimer2), "date": date.today().isoformat()}
          db.times.insert_one(mydict)

  if nameSwimmer3 != "" and millisTimer3 != "":
    age_group = ""
    gender = ""
    with open('names.csv') as csvfile:
      csvReader = csv.reader(csvfile)
      for row in csvReader:
        if row[0] == nameSwimmer3 and millisTimer3 != "":
          age = int(row[2])
          age_group = getAgeGroup(age)
          gender = row[1]
          mydict = { "name": nameSwimmer3, "gender": gender, "age_group": age_group, "stroke": strokeSwimmer3, "distance": distanceSwimmer3, "time": float(millisTimer3), "date": date.today().isoformat()}
          db.times.insert_one(mydict)
  return redirect(url_for('timer_page'))

def getAgeGroup(age):
  if age <= 6:
    return "6 and under"
  elif age <= 8:
    return "7-8"
  elif age <= 10:
    return "9-10"
  elif age <= 12:
    return "11-12"
  elif age <= 14:
    return "13-14"
  else:
    return "15 and older"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=random.randint(2000, 9000))
