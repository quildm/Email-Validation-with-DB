from flask import Flask, render_template, redirect, request, session, flash
# the "re" module will let us perform some regular expression operations
from mysqlconnection import MySQLConnector
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'email_list')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def submit():
    if request.form['email'] == '':
        flash("Email cannot be blank!")
        pass
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        pass 
    else:
        email = request.form['email']
        session['email'] = email
        query = "INSERT INTO email (email, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(session['email'])
        mysql.query_db(query)
    return render_template('success.html', emailed = email)







app.run(debug=True)

#  return redirect('/')