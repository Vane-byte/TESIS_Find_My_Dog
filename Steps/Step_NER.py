
from simpletransformers.ner import NERModel

#Reconocimiento de entidades (NER) del texto

def PredictNER(registro):
  
  model_saved=NERModel("bert",r'D:\Mis documentos\Documents\CLASES\tesiss\Codigo\Main Code\Helpers\Modelos\NEROutputs\outputs', use_cuda=False)

  predictions, raw_outputs=model_saved.predict([registro['descripcion']])
  predictions=predictions[0]
  resultado = [reg for reg in predictions if not any(valor == 'O' for valor in reg.values())]
  NER_dict={}
  for NER in resultado:
    NER_val= [NER[key] for key in NER][0]
    if NER_val in NER_dict:
      NER_dict[NER_val]= NER_dict[NER_val] + ' ' + list(NER)[0]
    else:
      NER_dict[NER_val]= list(NER)[0]
  registro['NER']=NER_dict
  return registro

