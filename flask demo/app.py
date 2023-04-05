from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from tensorflow import keras
from flask import flash

cooksmartapp = Flask(__name__)
bcrypt = Bcrypt(cooksmartapp)

# Set up the MongoDB client and database

client = MongoClient(
    "mongodb+srv://savinthie:cookSmart25@cluster0.zg9e7jn.mongodb.net/test")
db = client["cooksmart"]   #Conneted Cook Smart app to the database
collection = db["signup_infos"]
collection1 = db['recipeAndIngredientsGenerator']
cooksmartDirectory = 'flask demo/resnet-model-23-02-21.h5'
cooksmartModel = keras.models.load_model(
    cooksmartDirectory)  # loaded the cooksmart trained model
imageSize = (224, 224)

# list of food items in the dataset
FOOD_CLASSES = {
    0: 'Adhirasam',
    1: 'Aloo Gobi',
    2: 'Aloo Matar',
    3: 'Aloo Methi',
    4: 'Aloo Shimla Mirch',
    5: 'Aloo Tikki',
    6: 'Anarsa',
    7: 'Ariselu',
    8: 'Bandar Laddu',
    9: 'Basundi',
    10: 'Bhatura',
    11: 'Bhindi Masala',
    12: 'Biryani',
    13: 'Boondi',
    14: 'Butter Chicken',
    15: 'Chak Hao kheer',
    16: 'Cham Cham',
    17: 'Chana Masala',
    18: 'Chapati',
    19: 'Chhena kheeri',
    20: 'Chicken Razala',
    21: 'Chicken Tikka',
    22: 'Chicken Tikka Masala',
    23: 'Chikki',
    24: 'Daal Baati Churma',
    25: 'Daal Puri',
    26: 'Dal Makhani',
    27: 'Dal Tadka',
    28: 'Dharwad Pedha',
    29: 'Doodhpak',
    30: 'Double Ka Meetha',
    31: 'Dum Aloo',
    32: 'Gajar Ka Halwa',
    33: 'Gavvalu',
    34: 'Ghevar',
    35: 'Gulab Jamun',
    36: 'Imarti',
    37: 'Jalebi',
    38: 'Kachori',
    39: 'Kadai Paneer',
    40: 'Kadhi Pakoda',
    41: 'Kajjikaya',
    42: 'Kakinada Khaja',
    43: 'Kalakand',
    44: 'Karela Bharta',
    45: 'Kofta',
    46: 'Kuzhi Paniyaram',
    47: 'Lassi',
    48: 'Ledikeni',
    49: 'Litti Chokha',
    50: 'Lyangcha',
    51: 'Maach Jhol',
    52: 'Makki Di Roti Sarson Da Saag',
    53: 'Malapua',
    54: 'Misi Roti',
    55: 'Misti Doi',
    56: 'Modak',
    57: 'Mysore Pak',
    58: 'Naan',
    59: 'Nnavrattan Korma',
    60: 'Palak Paneer',
    61: 'Paneer Butter Masala',
    62: 'Phirni',
    63: 'Pithe',
    64: 'Poha',
    65: 'Poornalu',
    66: 'Pootharekulu',
    67: 'Qubani Ka Meetha',
    68: 'Rabri',
    69: 'Ras Malai',
    70: 'Rasgulla',
    71: 'Sandesh',
    72: 'Shankarpali',
    73: 'Sheer Korma',
    74: 'Sheera',
    75: 'Shrikhand',
    76: 'Sohan Halwa',
    77: 'Sohan Papdi',
    78: 'Sutar Feni',
    79: 'Unni Appam'
}


# function to predict the foodimage
def predict_image_class(foodImage_path):
    foodImage = keras.preprocessing.image.load_img(
        foodImage_path, target_size=imageSize)

    cooksmartImage_array = keras.preprocessing.image.img_to_array(foodImage)
    cooksmartImage_array = cooksmartImage_array.reshape(
        (1, cooksmartImage_array.shape[0], cooksmartImage_array.shape[1], cooksmartImage_array.shape[2]))
    predictions = cooksmartModel.predict(cooksmartImage_array)
    cooksmart_prediction_class = predictions.argmax(axis=1)[0]
    cooksmartPrediction_accuracy = predictions[0][cooksmart_prediction_class] * 100
    cooksmartPrediction_accuracy = f"{round(cooksmartPrediction_accuracy, 2)} %"

    predicted_food_name = FOOD_CLASSES[cooksmart_prediction_class]

    # return the predicted foodname
    return FOOD_CLASSES[cooksmart_prediction_class]

    # query the database for the recipe and ingredients of the predicted food


# routes
# route for the homepage, the page right after the signup or login credentials are entered
@cooksmartapp.route("/home", methods=['GET', 'POST'])
def main():
    return render_template("home.html")


predicted_food_name = ""  # declare a global variable to store the predicted food name
ingredient = ""
allergycount = 0
p = ""

#route for the image upload page
@cooksmartapp.route("/submitPrediction", methods=['GET', 'POST'])
def get_output():
    global p
    global predicted_food_name  # reference the global variable
    global ingredient
    global allergycount

    if request.method == 'POST':
        foodImage = request.files['cooksmartFood_image']

        # created a static folder to store the images that is being uploaded by the user
        foodImage_path = "flask demo/static/images/" + foodImage.filename

        foodImage.save(foodImage_path)
        p = predict_image_class(foodImage_path)
        print(p)
        predicted_food_name = p  # assign the predicted food name to the global variable

        # find the predicted food name in the db
        result = collection1.find_one({'foodName': p})
        recipe = result['Recipe']  # found the recipe for the foodname
        ingredient = result['ingredients']

    # return the prediction result to the frontend
    return render_template("recipe.html", prediction=predicted_food_name, recipe=recipe, ing=ingredient)


allergy_list = []

#route  for ingrdient selection page
@cooksmartapp.route('/allergy_list', methods=['POST'])
def allergy_list():
     # getting data from the POST request
    data = request.get_json()          
    global allergy_list
    # extracting allergy list from the received data
    allergy_list = data.get('allergy_list')   

    # do something with allergy_list
     # printing values of predicted_food_name and ingredient variables
    print(predicted_food_name)                    
    print(ingredient)                      
     
    # iterating through allergy_list and checking if the user entered allergen is present in the ingredient list
    for i in allergy_list:                 
        global allergycount
        allergycount=0
        print(i)
        # find the index of the user entered allergen
        if (ingredient.find(i) != -1):  
            print("allergen is there")
            allergycount += 1
            print(allergycount)
        else:
            # reset allergycount to 0
            allergycount == 0                
            print("allergen is not there")

    # rendering the notification.html template 
    return render_template("notification.html")       


message = ""

#route for notification 
@cooksmartapp.route("/allergyNotification")
def viewnew():
    global message
    print('allergycount',allergycount)
    if (allergycount > 0):
        message = "Yes"

    else:
        message = "None"

    return render_template("notification.html", message=message)

#route for notification display
@cooksmartapp.route("/viewAllergy")
def viewAllergy():
    return render_template("allergies.html")


"""@cooksmartapp.route("/presentation")
def predictionPage():
    return render_template("index.html")"""

# signup and  login


@cooksmartapp.route("/")
def index():
    return render_template("index.html")

#signup
@cooksmartapp.route("/submit", methods=["POST"])
def submit():
    # Get the data from the request
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    if collection.find_one({"$or": [{"username": username}, {"email": email}, {"password": password}]}):
        return "Username or email already taken", 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert the data into the MongoDB collection
    document = {"username": username,
                "email": email, "password": hashed_password}
    collection.insert_one(document)

    # Redirect to the success page
    return redirect('/home')



#route for signup page
@cooksmartapp.route('/signup')
def signupfun():
    return render_template('signup.html')

#route for display home page
@cooksmartapp.route('/home')
def home():
    return render_template('home.html')

#route for login page
@cooksmartapp.route('/login')
def another_page():
    return render_template('login.html')

#route for submit login
@cooksmartapp.route("/submit_login", methods=["POST"])
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
    cooksmartapp.run(debug=True)
