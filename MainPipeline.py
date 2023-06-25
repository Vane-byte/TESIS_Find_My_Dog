from Steps.Step_TextExtraction import ExtractTextFromImage
from Steps.Step_ImageClasification import predimage,recognitionDog
from Steps.Step_NER import PredictNER
from Steps.Step_TextClasification import DogStateClasification



#Validar si hay descripci?n en el registro

def processPerritos (registro):
  if  registro['descripcion']== '':
    registro= ExtractTextFromImage(registro)


  print("Inicio de clasificaci?n de publicaci?n ")
  print("_______________________________________")
  registro=DogStateClasification(registro)


  print("Inicio de reconocimiento de atributos ")
  print("_______________________________________")
  registro=PredictNER(registro)


  print("Inicio de reconocimiento de raza ")
  print("_______________________________________")
  registro=recognitionDog(registro)
  return registro

def buildPerritos(collection):
  lost_dogs=[]
  found_dogs=[]
  for dog in collection:
    registro={
      'descripcion':'',
      'imagen': dog['data'],
      'name': dog['name']
    }
    perrito=processPerritos(registro)
    if perrito['SePerdio']==1:
      lost_dogs.append(perrito)
    else:
      found_dogs.append(perrito)

  return lost_dogs,found_dogs
