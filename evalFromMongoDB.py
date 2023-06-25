import pymongo
from MainPipeline import processPerritos
from registerEvaluation import calTotal

# Connect to the MongoDB database

if __name__== '__main__':

     client = pymongo.MongoClient("mongodb+srv://20180841:mateito22@cluster0.wjkw5cx.mongodb.net/")
     db = client["Tesis"]
     hot_dogs_lost = db["Hot_Dogs_Lost"]
     hot_dogs_found = db["Hot_Dogs_Found"]

     ###BORRAR#######
     with open(r'D:\Mis documentos\Downloads\perritos\fbimage8.jpg', "rb") as f:
        image_data = f.read()
     ################
     received_arg= {'descripcion':'Encontramos a Lucky', 'imagen':image_data} #sys.argv[1]

     perrito= processPerritos(received_arg)
     
     if perrito['SePerdio']==1:
          all_regs=db["Hot_Dogs_Found"].find()
     else:
          all_regs=db["Hot_Dogs_Lost"].find()
     
     updated_regs=calTotal(all_regs, perrito)
     for reg in updated_regs:
          print(reg['name'],': ',reg['final_punctuation'])
