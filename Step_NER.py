from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,f1_score,confusion_matrix,recall_score
from simpletransformers.ner import NERModel,NERArgs
from keras.models import load_model

#Reconocimiento de entidades (NER) del texto
model_saved=NERModel("bert","D:\\Mis documentos\\Documents\\CLASES\\tesiss\\Codigo\\ALL\\Helpers\\Modelos\\NEROutputs\\outputs", use_cuda=False)

def PredictNER(registro):
  predictions, raw_outputs=model_saved.predict([registro['descripcion']])
  predictions=predictions[0]
  resultado = [registro for registro in predictions if not any(valor == 'O' for valor in registro.values())]
  NER_dict={}
  for NER in resultado:
    NER_val= [NER[key] for key in NER][0]
    if NER_val in NER_dict:
      NER_dict[NER_val]= NER_dict[NER_val] + ' ' + list(NER)[0]
    else:
      NER_dict[NER_val]= list(NER)[0]
  registro["NER"]=NER_dict
  return registro