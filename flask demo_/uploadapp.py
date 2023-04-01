from tensorflow import keras
from flask import Flask, render_template, request


cooksmartapp = Flask(__name__)

cooksmartDirectory = 'flask demo/resnet-model-23-02-21.h5'
cooksmartModel = keras.models.load_model(cooksmartDirectory)#loaded the cooksmart trained model
imageSize = (224, 224)

#list of food items in the dataset
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
14: 'Butter chicken',
15: 'Chak Hao Kheer',
16: 'Cham Cham',
17: 'Chana Masala',
18: 'Chapati',
19: 'Chhena Kheeri',
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
59: 'Navrattan Korma',
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




#function to predict the foodimage
def predict_image_class(foodImage_path):
    foodImage = keras.preprocessing.image.load_img(foodImage_path, target_size=imageSize)
    
    
    cooksmartImage_array = keras.preprocessing.image.img_to_array(foodImage)
    cooksmartImage_array = cooksmartImage_array.reshape((1, cooksmartImage_array.shape[0], cooksmartImage_array.shape[1], cooksmartImage_array.shape[2]))
    predictions = cooksmartModel.predict(cooksmartImage_array)
    cooksmart_prediction_class = predictions.argmax(axis=1)[0]
    cooksmartPrediction_accuracy = predictions[0][cooksmart_prediction_class] * 100
    cooksmartPrediction_accuracy = f"{round(cooksmartPrediction_accuracy, 2)} %"

    return FOOD_CLASSES[cooksmart_prediction_class]#return the predicted food name from the food class dictionary
#if accuracy is required :return cooksmartPrediction_accuracy


# routes
@cooksmartapp.route("/", methods=['GET', 'POST'])
def main():
	return render_template("home.html")

@cooksmartapp.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		foodImage = request.files['cooksmartFood_image']

		foodImage_path = "flask demo/static/images/" + foodImage.filename	#created a static folder to store the images that is being uploaded by the user
		foodImage.save(foodImage_path)

		p = predict_image_class(foodImage_path)
#image is not displayed due to a path error but result is displayed : -should fix it .(savinthie)
	return render_template("home.html", prediction = p, foodImage_path = foodImage_path)#return the prediction result to the frontend


if __name__ =='__main__':
	#cooksmartapp.debug = True
	cooksmartapp.run(debug = True)