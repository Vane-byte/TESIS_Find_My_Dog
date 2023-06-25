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
  dogs=[]
  for dog in collection:
    registro={
      'descripcion':'',
      'imagen': dog['data']
    }
    dogs.append(processPerritos(registro))
    return dogs
