import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["SmartCook"]
collection = db["Food Ingredient"]

user = input("Enter Food_name:")

document = collection.find_one({"foodName":user})
print(document)


