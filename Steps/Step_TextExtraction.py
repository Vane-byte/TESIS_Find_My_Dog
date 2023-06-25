import easyocr
import cv2
import matplotlib.pyplot as plt

#RECONOCIMIENTO DE TEXTO EN IMÁGENES
ocr=easyocr.Reader(['es'])

def ExtractTextFromImage(registro):
  #img2=cv2.imread(registro['imagen'])
  result=ocr.readtext(registro['imagen'])

  DescImg = []
  for r in result:
    DescImg.append(r[1]+" ")
  print("texto:", ''.join(DescImg))
  registro['descripcion']=''.join(DescImg)
  return registro

