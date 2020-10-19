from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector #pip3 install mysql-connector
import os

mydb = mysql.connector.connect(host='localhost', user='codeworked', passwd='elephant', database='sample', auth_plugin='mysql_native_password')

cursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(30)

@app.route('/')
def index():
    title = 'GymTrack - Home'
    return render_template('home.html', title = title)



@app.route('/signup', methods=['post', 'get'])
def signup():
    error=None
    success=None
    if request.method=='POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if len(phone_number)>11:
            error="Enter your phone number correctly"
        elif len(password)<6:
            error="Password should have atleast 6 characters"
        elif password != confirm_password:
            error="Password do not match"
        else:
            query = "INSERT INTO users(id, first_name, last_name, email, phone, password, date) VALUES (NULL, %s, %s, %s, %s, %s, NOW())"
            cursor.execute(query, (first_name, last_name, email, phone_number, password))
            mydb.commit()
            success = "Your account has been created"

    signuptitle = 'GymTrack - Sign Up'
    return render_template('signup.html', title3 = signuptitle, error=error, msg=success)

@app.route('/login', methods=['post', 'get'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if len(password)<6:
            error = "Password Invalid"
        else:
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            rows = cursor.fetchall()
            countRows = cursor.rowcount
            if countRows < 1:
                error = "Invalid Login Details"
            else:
                session['email'] = email
                return redirect(url_for('mytracking'))

    tracktitle = 'GymTrack - Login'
    return render_template('login.html',  title4 = tracktitle, error=error)

@app.route('/mytracking', methods=['post', 'get'])
def mytracking():
    email = session.get("email")
    if request.method == 'POST':
        date = request.form.get("date")
        exercises = request.form.get("exercises")
        weight = request.form.get("weight")
        sets = request.form.get("sets")
        reps = request.form.get("reps")
        time = request.form.get("time")
        query = "INSERT INTO gym(id, date, exercises, weight, sets, reps, time) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (date, exercises, weight, sets, reps, time))
        mydb.commit()

    query = "SELECT * FROM gym"
    cursor.execute(query)
    rows = cursor.fetchall()

    if email is None:
        return redirect(url_for('login'))
    tracktitle = 'GymTrack - My Tracking'
    return render_template('track.html',  title2 = tracktitle, email=email, result=rows)

#@app.route('/<first_name>', methods=('post', 'get'))
#def profile(first_name):
    #name=users.objects.filter(first_name=first_name)
    #title = 'GymTrack'
    #return render_template('first_name/profile.html', title = title)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug = True)
