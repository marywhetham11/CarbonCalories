# register: enters user in account database
# login: checks if user is in account database, returns success or not success

from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
#import MySQLdb
import os
import datetime
import json

#import mysql.connector

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

def connection():
    unix_socket = '/cloudsql/{}'.format(os.environ.get('CLOUDSQL_DSN'))
    conn = MySQLdb.connect(user=os.environ.get('CLOUDSQL_USER'), passwd=os.environ.get('CLOUDSQL_PASSWORD'), db=os.environ.get('CLOUDSQL_DB'), unix_socket=unix_socket)
    c = conn.cursor()

    return c, conn

def calculateRating(productID):
    mycursor, conn = connection()

    mycursor.execute("SELECT * FROM products where productID = " + str(productID) + ";")
    products = mycursor.fetchone()

    columnWeights = [0.3, 0.2, 0.1, 0.3, 0.1]
    score = 0

    score1=0
    score2=0
    score3=100
    score4=100
    score5=0

    # Local Calculation
    if products[3] == 1:
        score1 = 100
    else:
        score1 = 0
    
    # Plant Based Calculation
    if products[4] == 1:
        score2 = 100
    elif products[4] == 2:
        score2 = 50
    else:
        score2 = 0
    
    # Packaging Calculation
    packaging = str(products[5]).split()
    j = 0
    while j < len(packaging):
        if 'Plastic' in packaging[j]:
            print("We here bishes")
            score3 = score3 - 30
        if 'Paper' in packaging[j]:
            score3 = score3 - 10
        if 'Styrofoam' in packaging[j]:
            score3 = score3 - 15
        if 'Glass' in packaging[j]:
            score3 = score3 - 20
        if 'Metal' in packaging[j]:
            score3 = score3 - 25
        j = j+1
    
    # Meat Calculation
    if products[6] == 'Red':
        score4 = score4 - 90
    elif products[6] == 'White':
        score4 = score4 - 30
    
    # Seasonal Calculation
    if products[7] == 1:
        score5 = 0
    elif products[7] == 0:
        score5 = 100

    score = ((score1 * columnWeights[0]) + (score2 * columnWeights[1]) + (score3 * columnWeights[2]) + (score4 * columnWeights[3]) + (score5 * columnWeights[4])) / 10
    
    conn.close()
    
    return score

@app.route('/', methods=['GET'])
def render_home():
    if 'username' in session:
        return render_template('HomeLoggedIn.html', username=session.get('username'))
    else:
        return render_template('Home.html')

@app.route('/faq', methods=['GET'])
def render_faq():
    if 'username' in session:
        return render_template('FAQLoggedIn.html', username=session.get('username'))
    else:
        return render_template('FAQ.html')

@app.route('/login', methods=['GET'])
def render_login():
    if 'username' in session:
        return redirect('/profile')
    else:
        return render_template('Log in.html', message=None)

@app.route('/profile', methods=['GET'])
def render_profile():
    if 'username' in session:
        cur, conn = connection()

        cur.execute("SELECT avg(score) from history where account_id =" + str(session.get('user_id')) + ";")
        result = cur.fetchone()
        if not result[0]:
            yourScore = 0.0
        else:
            yourScore = float("{:.1f}".format(result[0]))

        cur.execute("SELECT avg(score) from history;")
        result = cur.fetchone()
        if not result[0]:
            avgScore = 0.0
        else:
            avgScore = float("{:.1f}".format(result[0]))

        conn.close()

        if yourScore > avgScore:
            message = "Your carbon score is higher than the average carbon score! Congratulations! We all need to keep our score as high as possible, so keep up the good work!"
        elif yourScore < avgScore:
            message = "Great effort! However, your carbon score is lower than the average carbon score. To increase this, try to buy products with a higher score!"
        else:
            message = "Great effort! Your carbon score is equal than the average carbon score. To increase this, try to buy products with a higher score!"

        return render_template('Profile.html', username=session.get('username'), yourScore=yourScore, avgScore=avgScore, message=message)
    else:
        # mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="",
        #     database="carbon_calories"
        # )

        # cur = mydb.cursor()

        # cur.execute("SELECT avg(score) from history where account_id = 1;")
        # yourScore = cur.fetchone()
        # if cur.rowcount == 0:
        #     yourScore = float("{:.1f}".format(yourScore[0]))
        # else:
        #     yourScore = 0.0

        # cur.execute("SELECT avg(score) from history;")
        # avgScore = cur.fetchone()
        # if cur.rowcount == 0:
        #     avgScore = float("{:.1f}".format(avgScore[0]))
        # else:
        #     avgScore = 0.0
        # if yourScore > avgScore:
        #     message = "Your carbon score is higher than the average carbon score! Congratulations! We all need to keep our score as high as possible, so keep up the good work!"
        # elif yourScore < avgScore:
        #     message = "Great effort! However, your carbon score is lower than the average carbon score. To increase this, try to buy products with a higher score!"
        # else:
        #     message = "Great effort! Your carbon score is equal than the average carbon score. To increase this, try to buy products with a higher score!"

        # return render_template('Profile.html', username=session.get('username'),  yourScore=yourScore, avgScore=avgScore, message=message)
        return redirect('/')

@app.route('/history', methods=['GET'])
def render_history():
    if 'username' in session:
        cur, conn = connection()
        cur.execute("SELECT * from history where account_id =" + str(session.get('user_id')) + ";")
        result = cur.fetchall()

        products = []
        for item in result:
            cur.execute("SELECT productName from products where productID =" + str(item[2]) + ";")
            result2 = cur.fetchone()
            products.append(result2[0])

        conn.close()

        return render_template('History.html', username=session.get('username'), history=result, products=products, length=len(result))
    else:
        #return render_template('History.html', username=session.get('username'), history=None, products=None, length=0)
        return redirect('/')

@app.route('/analytics', methods=['GET'])
def render_analytics():
    if 'username' in session:
        cur, conn = connection()

        cur.execute("SELECT count(history.productId) from history inner join products on history.productId = products.productID where account_id =" + str(session.get('user_id')) + " and local = 1;")
        local = cur.fetchone()

        cur.execute("SELECT count(history.productId) from history inner join products on history.productId = products.productID where account_id =" + str(session.get('user_id')) + " and local = 0;")
        non_local = cur.fetchone()

        cur.execute("SELECT count(history.productId) from history inner join products on history.productId = products.productID where account_id =" + str(session.get('user_id')) + " and plantBased = 0;")
        meat = cur.fetchone()

        cur.execute("SELECT count(history.productId) from history inner join products on history.productId = products.productID where account_id =" + str(session.get('user_id')) + " and plantBased = 1;")
        plant = cur.fetchone()

        cur.execute("SELECT count(history.productId) from history inner join products on history.productId = products.productID where account_id =" + str(session.get('user_id')) + " and plantBased = 2;")
        other = cur.fetchone()

        cur.execute("SELECT avg(history.score), date from history where account_id =" + str(session.get('user_id')) + " group by date")
        yourHistory = cur.fetchall()

        cur.execute("SELECT avg(history.score), date from history group by date")
        averageHistory = cur.fetchall()

        pie1 = [{
            'type': 'Local',
            'quantity': local[0],
            'color': "#5120DB"
        }, {
            'type': 'Non-Local',
             'quantity': non_local[0],
            'color': "#DB209B"
        }]

        pie2 = [{
            'type': 'Meat-based',
            'quantity': meat[0],
            'color': "#2ECE5B"
        }, {
            'type': 'Plant-based',
            'quantity': plant[0],
            'color': "#2EB1CE"
        }, {
            'type': 'Other',
            'quantity': other[0],
            'color': "#CE682E"
        }]

        line1 = []
        for line in yourHistory:
            line1.append({"date": line[1], "value": float("{:.2f}".format(line[0]))})

        line2 = []
        for line in averageHistory:
            line2.append({"date": line[1], "value": float("{:.2f}".format(line[0]))})

        conn.close()

        return render_template('Analytics.html', pie1=pie1, pie2=pie2, line1=line1, line2=line2, username=session.get('username'))
    else:
        # pie1 = [{
        #     'type': 'Local',
        #     'quantity': 3,
        #     'color': "#5120DB"
        # }, {
        #     'type': 'Non-Local',
        #      'quantity': 4,
        #     'color': "#DB209B"
        # }]

        # pie2 = [{
        #     'type': 'Meat-based',
        #     'quantity': 5,
        #     'color': "#2ECE5B"
        # }, {
        #     'type': 'Plant-based',
        #     'quantity': 6,
        #     'color': "#2EB1CE"
        # }, {
        #     'type': 'Other',
        #     'quantity': 7,
        #     'color': "#CE682E"
        # }]

        # line1 = []

        # line2 = []

        # #conn.close()

        # return render_template('Analytics.html', pie1=pie1, pie2=pie2, line1=line1, line2=line2, username=session.get('username'))
        return redirect('/')

@app.route('/search', methods=['GET'])
def render_search():
    if 'username' in session:
        return render_template('Search.html', username=session.get('username'), products=[])
    else:
        #return render_template('Search.html', username=session.get('username'), products=[])
        return redirect('/')

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        details = request.form
        productID = details['search']

        cur, conn = connection()
        cur.execute("SELECT * FROM products where productName like '%"+ str(productID) + "%';")
        products = cur.fetchall()

        result = []
        for product in products:
            result.append([product[1], calculateRating(product[2])])

        conn.close()

        return render_template('Search.html', username=session.get('username'), products=result, message=None)

@app.route('/settings', methods=['GET'])
def render_settings():
    if 'username' in session:
        cur, conn = connection()
        cur.execute("SELECT * from account where username = (%s)", (session.get('username'),))
        result = cur.fetchone()
        conn.close()
        return render_template('Settings.html', username=session.get('username'), details=result, message=None)
    else:
        #return render_template('Settings.html', username=session.get('username'), details=None, message=None)
        return redirect('/')

@app.route('/logout', methods=['GET'])
def render_logout():
    if 'username' in session:
        session['loggedin'] = False
        session.pop('username')
    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        details = request.form
        username = details['username']
        email = details['email']
        location = details['location']
        address = details['address']
        password = details['password']
        cur, conn = connection()
        cur.execute("UPDATE account set username = '" + username + "', email = '" + email + "', location = '" + location + "', address = '" + address + "', password = '" + password + "' where id = " + str(session.get('user_id')) + ";")
        conn.commit()

        cur.execute("SELECT * from account where username = (%s)", (session.get('username'),))
        result = cur.fetchone()
        conn.close()
        return render_template('Settings.html', username=session.get('username'), details=result, message="Your account has been updated!")

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        details = request.form
        username = details['username']
        email = details['email']
        location = details['location']
        address = details['address']
        password = details['password']
        cur, conn = connection()
        cur.execute("INSERT INTO account(username, email, location, address, password) VALUES (%s, %s, %s, %s, %s)", (username, email, location, address, password))
        conn.commit()

        cur.execute("SELECT * from account where username = %s and password = %s", (username, password))
        result = cur.fetchone()
        session['loggedin'] = True
        session['username'] = username
        session['user_id'] = result[0]

        conn.close()
        return redirect('/profile')

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        details = request.form
        username = details['username']
        password = details['password']
        cur, conn = connection()
        cur.execute("SELECT * from account where username = %s and password = %s", (username, password))
        result = cur.fetchone()

        if result != None:
            session['loggedin'] = True
            session['username'] = username
            session['user_id'] = result[0]
            conn.close()
            return redirect('/profile')
        else:
            return render_template('Log in.html', message="Incorrect username or password")
        

@app.route('/loginpopup', methods=['POST'])
def login_popup():
    if request.method == "POST":
        details = request.get_json()
        username = details['username']
        password = details['password']
        cur, conn = connection()
        cur.execute("SELECT * from account where username = %s and password = %s", (username, password))
        result = cur.fetchone()
        if result != None:
            response = jsonify(message="success")
        else:
            response = jsonify(message="not success")
        conn.close()
        return response

@app.route('/getscores', methods=['POST'])
def get_scores():
    if request.method == "POST":
        details = request.get_json()
        ids = details['ids']
        scores = []
        for item in ids:
            scores.append(calculateRating(int(item)))

        response = jsonify(scores=scores)
        return response

@app.route('/submitscores', methods=['POST'])
def submit_scores():
    if request.method == "POST":
        details = request.get_json()

        cur, conn = connection()

        cur.execute("SELECT id from account where username = (%s)", (details['username'],))
        result = cur.fetchone()
        account_id = result[0]
        
        ids = details['ids']
        item_score = details['item_scores']
        x = datetime.datetime.now()
        dateToday = x.strftime('%Y-%m-%d')
        
        for i in range(len(ids)):
            product_id = int(ids[i])
            score = item_score[i]
            cur.execute("INSERT INTO history(account_id, productId, score, date) VALUES (" + str(account_id) + ", " + str(product_id) + ", " + str(score) + ", '" + dateToday + "');")
            conn.commit()

        conn.close()
        response = jsonify(message="success")
        return response

app.run()
