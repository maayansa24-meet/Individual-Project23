from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyAzZoEy0H-H6plWLDHc6swXB91IOu36Yoc",
  "authDomain": "cs-prog.firebaseapp.com",
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



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the input values from the form
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            full_name = request.form['full_name']
            username = request.form['username']
            bio = request.form['bio'][:280]  # Truncate to a maximum of 280 characters

            # Create a dictionary with user information
            user = {
                'full_name': full_name,
                'username': username,
                'bio': bio
            }

            # Add the user to the database using their uid (retrieve it through login_session)
            uid = login_session['user']['localId']  # Replace with the actual way of retrieving the uid
            db.child('Users').child(uid).set(user)
            return redirect(url_for('/'))
        except:
            error = "Authentication failed"



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)