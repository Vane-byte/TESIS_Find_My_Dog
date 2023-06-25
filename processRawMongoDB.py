import pymongo
from glob import glob
from MainPipeline import buildPerritos
# Connect to the MongoDB database
img_fns = glob('D:/Mis documentos/Documents/CLASES/tesiss/Codigo/ALL/perritos/*')   

client = pymongo.MongoClient("mongodb+srv://20180841:mateito22@cluster0.wjkw5cx.mongodb.net/")
db = client["Tesis"]
collection = db["Raw_dogs"]
hot_dogs_lost = db["Hot_Dogs_Lost"] 
hot_dogs_found = db["Hot_Dogs_Found"]

# Delete all documents from the collection
hot_dogs_lost.delete_many({})
hot_dogs_found.delete_many({})


# Insert the document into the collection
col=[collection.find_one({})]   
dogs=buildPerritos(col)

for dog in dogs:
    print(dog)
    

# Close the connection
client.close()