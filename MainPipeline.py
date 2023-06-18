from Step_TextExtraction import ExtractTextFromImage
from Step_ImageClasification import predimage
from Step_NER import PredictNER
from Step_TextClasification import DogStateClasification

#Validar si hay descripción en el registro


registro={
    'descripcion':'',
    'imagen':'/content/drive/MyDrive/TESI/perritos/fbimage.jpg'
}
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
registro=predimage(registro)