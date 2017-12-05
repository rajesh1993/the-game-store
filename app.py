from flask import Flask, render_template, redirect, url_for, request, json
from flaskext.mysql import MySQL
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ecommercedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
loggedUser = None

@app.route('/')
def home():
	global loggedUser
	return render_template("index.html", logUser = loggedUser)

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	global loggedUser
	if loggedUser:
		return redirect(url_for('home'))
	if request.method == 'POST':
		userID = request.form['username']
		password = request.form['password']
		query = "SELECT Username FROM User where Username = '" + userID + "' and Password = '" + password + "';"
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(query)
		data = cursor.fetchone()
		conn.close()
		if not data:
			error = 'Invalid Credentials'
		else:
			loggedUser = userID
			return redirect(url_for('home'))
	return render_template('login.html', error = error)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	global loggedUser
	if loggedUser != None:
		loggedUser = None
	return redirect(url_for('home'))

@app.route('/Authenticate')
def Authenticate():
	username = request.args.get('UserName')
	password = request.args.get('Password')
	conn = mysql.connect()
	cursor = conn.cursor()
	# cursor.execute("SELECT * from User where Username ='" + username + "' and Password='" + password + "'")
	cursor.execute("SELECT Username from User")
	data = cursor.fetchall()
	if username is None:
		return "Username or Password is wrong"
	else:
		return render_template('productFill.html', products = data)

@app.route('/showSignUp', methods = ['GET', 'POST'])
def showSignUp():
	global loggedUser
	if loggedUser:
		return redirect(url_for('home'))
	return render_template('signup.html')

@app.route('/signUp', methods = ['POST', 'GET'])
def signUp():
	# error = None
	firstName = request.form['inputFirstName']
	lastName = request.form['inputLastName']
	emailAdd = request.form['inputEmail']
	phoneno = request.form['inputPhone']
	streetAdd = request.form['inputAddress']
	userName = request.form['inputUserName']
	password = request.form['inputPassword']
	query = "INSERT INTO User(EmailID, Phone, FirstName, LastName, Address, Password, Username) VALUES('" + emailAdd + "'," + phoneno + ",'" \
	+ firstName + "','" + lastName + "','" + streetAdd + "','" + password + "','" + userName + "');"
	# validate the received values
	if firstName and emailAdd and password:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		conn.close()
		return redirect(url_for('home'))
	else:
		# error = "invalid entry"
		# return "Username or Password is wrong"
		return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	# except MySQLdb.IntegrityError:
	# 	error = 'Signup Failed. Try Again'
	# finally:
	# 	cursor.close()

@app.route('/products')
def productDisplay():
	conn = mysql.connect()
	cursor = conn.cursor()
	query = "SELECT ProductName, Category, Description, Colour FROM product;"
	cursor.execute(query)
	data = cursor.fetchall()
	return render_template('productFill.html', products = data)

@app.route('/productPage')
def productPage():
	productName = request.args.get('ProductName')
	category = request.args.get('Category')
	conn = mysql.connect()
	cursor = conn.cursor()
	query = "SELECT ProductName, Category, Description, Colour FROM product where ProductName = '" + productName + "' and Category='" + category + "';"
	cursor.execute(query)
	data = cursor.fetchone()
	query = "SELECT U.Username, R.Rating, R.Description, R.ReviewDate FROM Customer C, ProductHasReview H, Product P, Review R, User U WHERE H.CustomerID = C.CustomerID and P.ProductID = H.ProductID and R.ReviewID = H.ReviewID and C.CustomerID = U.userID and P.ProductName = '" + productName + "';"
	cursor.execute(query)
	reviewList = cursor.fetchall()
	return render_template('productPage.html', product = data, reviews = reviewList)

@app.route('/addProduct', methods = ['POST', 'GET'])
def addProduct():
	global loggedUser
	error = None
	success = None
	if request.method == 'POST':
		productName = request.form['inputProductName']
		category = request.form['categorySelect']
		desc = request.form['inputDesc']
		color = request.form['inputColor']
		query = "INSERT INTO Product(ProductName, Category, Description, Colour) VALUES ('" + productName + "','" + category + "','" + desc + "','" + color + "');"
		if productName and desc:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			conn.close()
			success = 1
		else:
			error = 'Invalid Product/Product already exists'
	return render_template('addProduct.html', error = error, success = success)

@app.route('/personalCart', methods = ['GET', 'POST'])
def personalCart():
	global loggedUser
	return render_template('personalCart.html')


if __name__ == "__main__":
	app.run(debug = True)