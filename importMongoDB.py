import pymongo
from glob import glob
# Connect to the MongoDB database
img_fns = glob('D:/Mis documentos/Documents/CLASES/tesiss/Codigo/ALL/perritos/*')   

client = pymongo.MongoClient("mongodb+srv://20180841:mateito22@cluster0.wjkw5cx.mongodb.net/")
db = client["Tesis"]
collection = db["Raw_dogs"]


# Delete all documents from the collection
collection.delete_many({})

documents=[]

# Read the image file and convert it to binary data
def convert_to_document(dog):
    print("perro",dog)
    with open(dog, "rb") as f:
        image_data = f.read()
    # Create a new document
    image_document = {
        "name": dog.split('\\')[1],
        "data": image_data
    }
    documents.append(image_document)

for dog in img_fns:
    convert_to_document(dog)
 
# Insert the document into the collection
collection.insert_many(documents)

# Close the connection
client.close()