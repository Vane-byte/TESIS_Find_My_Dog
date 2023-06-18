import easyocr
import cv2
import matplotlib.pyplot as plt

#RECONOCIMIENTO DE TEXTO EN IMÁGENES
ocr=easyocr.Reader(['es'])

def ExtractTextFromImage(registro):
  img2=cv2.imread(registro['imagen'])
  img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
  plt.imshow(img2_rgb)
  plt.axis('off')  # Desactivar los ejes
  plt.show()
  result=ocr.readtext(img2,gpu='cuda:0')

  DescImg = []
  for r in result:
    DescImg.append(r[1]+" ")
  print("texto:", ''.join(DescImg))
  registro['descripcion']=''.join(DescImg)
  return registro

