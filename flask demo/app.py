from flask import Flask, render_template, request,redirect
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Set up the MongoDB client and database
client = MongoClient("mongodb://localhost:27017")
db = client["SmartCook"]
collection = db["Signup_info"]

@app.route("/")
def index():
    return render_template("signup.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Get the data from the request
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    # Insert the data into the MongoDB collection
    document = {"username": username, "email": email, "password": hashed_password}
    collection.insert_one(document)

    # Redirect to the success page
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def another_page():
    return render_template('login.html')




if __name__ == "__main__":
    app.run(debug=True)
