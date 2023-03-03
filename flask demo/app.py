from flask import Flask, render_template, request,redirect,jsonify
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


    if collection.find_one({"$or": [{"username": username}, {"email": email},{"password":password}]}):
        return "Username or email already taken", 409


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

@app.route("/submit_login", methods=["POST"])
def submit_login():
    # Get the data from the request
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # Check if the username exists in the database
    user = collection.find_one({"username": username})
    if user is None:
        # Username not found
        return jsonify({"success": False}), 401

    # Check if the password matches
    if not bcrypt.check_password_hash(user["password"], password):
        # Password incorrect
        return jsonify({"success": False}), 401 
     # Redirect to the home page
     # Password correct
    return jsonify({"success": True})





if __name__ == "__main__":
    app.run(debug=True)
