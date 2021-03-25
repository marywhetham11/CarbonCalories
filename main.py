# register: enters user in account database
# login: checks if user is in account database, returns success or not success

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'carbon_calories_account'

mysql = MySQL(app)

@app.route('/register', methods=['GET'])
def render_register():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def render_login():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        details = request.form
        username = details['username']
        email = details['email']
        location = details['location']
        address = details['address']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO account(username, email, location, address, password) VALUES (%s, %s, %s, %s, %s)", (username, email, location, address, password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        details = request.form
        username = details['username']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from account where username = %s and password = %s", (username, password))
        mysql.connection.commit()
        result = cur.fetchone()
        if result != None:
            return 'success'
        else:
            return 'not success'
        cur.close()
    return render_template('login.html')

app.run(host='localhost', port=5000)


