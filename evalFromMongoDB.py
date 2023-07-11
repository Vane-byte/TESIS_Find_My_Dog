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
          perrito['SePerdio'] = 'Perro Perdido'
          all_regs=db["Hot_Dogs_Found"].find()
     else:
          perrito['SePerdio'] = 'Perro Encontrado'
          all_regs=db["Hot_Dogs_Lost"].find()
     
     updated_regs=calTotal(list(all_regs), perrito)
     df = pd.DataFrame(updated_regs)
     df=df.sort_values(by=['Total'], ascending= False)
     df=df.head(10)
     dict_list = df.to_dict('records')

     print(df[['name','NER_points','IMG_points']])
     print('NER: ',perrito['NER'], '\nRazas: ', perrito['imagen_razas'])
     return perrito, dict_list