import pymongo
from MainPipeline import processPerritos
from registerEvaluation import calTotal
import pandas as pd

# Connect to the MongoDB database

def finalEvaluation(registro):

     client = pymongo.MongoClient("mongodb+srv://20180841:mateito22@cluster0.wjkw5cx.mongodb.net/")
     db = client["Tesis"]

     perrito= processPerritos(registro)
     
     if perrito['SePerdio']==1:
          all_regs=db["Hot_Dogs_Found"].find()
     else:
          all_regs=db["Hot_Dogs_Lost"].find()
     
     updated_regs=calTotal(list(all_regs), perrito)

     df = pd.DataFrame(updated_regs)
     print(df[['name','NER_points','IMG_points']])
     print('NER: ',perrito['NER'], '\nRazas: ', perrito['imagen_razas'])
     return perrito, updated_regs