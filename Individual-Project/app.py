from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyAzZoEy0H-H6plWLDHc6swXB91IOu36Yoc",
  "authDomain": "cs-prog.firebaseapp.com",
  "databaseURL": "https://cs-prog-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "cs-prog",
  "storageBucket": "cs-prog.appspot.com",
  "messagingSenderId": "1020287998690",
  "appId": "1:1020287998690:web:f2908b4bc09694550b5cbb",
  "measurementId": "G-9D63W1WVT6",
  "databaseURL" : "https://cs-prog-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


# Route for the signup page
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            userName = request.form['userName']
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            uid = login_session['user']['localId']
            user = {"email": email, "password":password,"name":userName}
            db.child('Users').child(uid).set(user)
            return render_template('sign_in.html')  
        except:
            error = "Authentication failed"
            print(error)
    return render_template('sign_up.html')  

@app.route('/signin', methods=['GET', 'POST'])
def signin():
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"
           print(error)
   return render_template("sign_in.html")
@app.route('/home')
def home():
    uName = db.child('Users').child('user').child('name').get().val()
    return render_template('home.html', uName = uName)
@app.route('/products')
def products():
    return render_template('products.html')
@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_cart():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        UID = login_session['user']['localId']
        to_add = {
            'name': name,
            'price': price
        }
        db.child('Cart').push(to_add)
        return redirect('cart') 
    return render_template('cart.html')

# Route for displaying all tweets
@app.route('/all_tweets')
def all_tweets():
    # Get all the tweets from the database
    tweets = db.child('Tweets').get()

    return render_template('tweets.html', tweets = tweets)





#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)