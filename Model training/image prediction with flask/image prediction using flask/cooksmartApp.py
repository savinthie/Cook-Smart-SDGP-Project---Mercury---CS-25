from tensorflow import keras
from flask import Flask, render_template, request


cooksmartapp = Flask(__name__)

cooksmartDirectory = 'resnet-model-23-02-21.h5'
cooksmartModel = keras.models.load_model(cooksmartDirectory)#loaded the cooksmart trained model
imageSize = (224, 224)

#list of food items in the dataset
FOOD_CLASSES = {
0: 'adhirasam',
1: 'aloo_gobi',
2: 'aloo_matar',
3: 'aloo_methi',
4: 'aloo_shimla_mirch',
5: 'aloo_tikki',
6: 'anarsa',
7: 'ariselu',
8: 'bandar_laddu',
9: 'basundi',
10: 'bhatura',
11: 'bhindi_masala',
12: 'biryani',
13: 'boondi',
14: 'butter_chicken',
15: 'chak_hao_kheer',
16: 'cham_cham',
17: 'chana_masala',
18: 'chapati',
19: 'chhena_kheeri',
20: 'chicken_razala',
21: 'chicken_tikka',
22: 'chicken_tikka_masala',
23: 'chikki',
24: 'daal_baati_churma',
25: 'daal_puri',
26: 'dal_makhani',
27: 'dal_tadka',
28: 'dharwad_pedha',
29: 'doodhpak',
30: 'double_ka_meetha',
31: 'dum_aloo',
32: 'gajar_ka_halwa',
33: 'gavvalu',
34: 'ghevar',
35: 'gulab_jamun',
36: 'imarti',
37: 'jalebi',
38: 'kachori',
39: 'kadai_paneer',
40: 'kadhi_pakoda',
41: 'kajjikaya',
42: 'kakinada_khaja',
43: 'kalakand',
44: 'karela_bharta',
45: 'kofta',
46: 'kuzhi_paniyaram',
47: 'lassi',
48: 'ledikeni',
49: 'litti_chokha',
50: 'lyangcha',
51: 'maach_jhol',
52: 'makki_di_roti_sarson_da_saag',
53: 'malapua',
54: 'misi_roti',
55: 'misti_doi',
56: 'modak',
57: 'mysore_pak',
58: 'naan',
59: 'navrattan_korma',
60: 'palak_paneer',
61: 'paneer_butter_masala',
62: 'phirni',
63: 'pithe',
64: 'poha',
65: 'poornalu',
66: 'pootharekulu',
67: 'qubani_ka_meetha',
68: 'rabri',
69: 'ras_malai',
70: 'rasgulla',
71: 'sandesh',
72: 'shankarpali',
73: 'sheer_korma',
74: 'sheera',
75: 'shrikhand',
76: 'sohan_halwa',
77: 'sohan_papdi',
78: 'sutar_feni',
79: 'unni_appam'
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
	return render_template("index.html")

@cooksmartapp.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		foodImage = request.files['cooksmartFood_image']

		foodImage_path = "static/" + foodImage.filename	#created a static folder to store the images that is being uploaded by the user
		foodImage.save(foodImage_path)

		p = predict_image_class(foodImage_path)

	return render_template("index.html", prediction = p, foodImage_path = foodImage_path)#return the prediction result to the frontend


if __name__ =='__main__':
	#cooksmartapp.debug = True
	cooksmartapp.run(debug = True)



