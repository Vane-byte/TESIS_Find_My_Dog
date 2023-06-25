from io import BytesIO
import tensorflow as tf
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.preprocessing.image import load_img 
from tensorflow.keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2
from PIL import Image
import decimal 

import numpy as np
import tempfile

new_model = tf.keras.models.load_model('D:\Mis documentos\Documents\CLASES\\tesiss\Codigo\Main Code\Helpers\Modelos\RESENTV2_Last.h5')

IMG_SIZE = 299
INIT_LR = 1e-5
EPOCHS = 20
BS = 32
class_names = ['n02086240-Shih-Tzu','n02086079-Pekinese','n02097209-standard_schnauzer','n02097047-miniature_schnauzer','n02102318-cocker_spaniel','n02110958-pug','n02088364-beagle','n02085620-Chihuahua','n02099601-golden_retriever',
    'n02112018-Pomeranian','n02108089-boxer','n02110185-Siberian_husky','n02113624-toy_poodle','n02106550-Rottweiler','n02108915-French_bulldog','n02113712-miniature_poodle','n02107142-Doberman',
    'n02099712-Labrador_retriever','n02093256-Staffordshire_bullterrier','n02096585-Boston_bull','n02097474-Tibetan_terrier','n02102177-Welsh_springer_spaniel','n02087046-toy_terrier','n02095314-wire-haired_fox_terrier','n02106166-Border_collie',
    'n02089867-Walker_hound','n02101388-Brittany_spaniel','n02106662-German_shepherd','n02094433-Yorkshire_terrier','n02093428-American_Staffordshire_terrier','n02085936-Maltese_dog']

def recognitionDog(registro):
    bit_img=Image.open(BytesIO(registro['imagen']))
    model_objectDetect = YOLO(r'D:\Mis documentos\Documents\CLASES\tesiss\Codigo\Main Code\Helpers\Modelos\yolov8n.pt')
    results = model_objectDetect.predict(source=bit_img, classes=[16, 1])

    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_file.write(registro['imagen'])

    img = cv2.imread(temp_file.name)

    for result in results:
        boxes = result.boxes.cpu().numpy()
        for i, box in enumerate(boxes):
            r = box.xyxy[0].astype(int)
            crop = img[r[1]:r[3], r[0]:r[2]]
            if i == 0:
                _, buffer = cv2.imencode('.png', crop)
                registro['imagen']=buffer.tobytes()
                print("----------------------")
                print("dog recognition finish")
                print("----------------------")
    registro=predimage(registro)
    return registro


def predimage(registro):
    image=Image.open(BytesIO(registro['imagen']))
    test = image.resize((299, 299))
    test = img_to_array(test)
    test = np.expand_dims(test, axis=0)
    test /= 255
    result = new_model.predict(test, batch_size=BS)
    top_classes = np.argsort(result, axis=1)[0, -3:][::-1]
    top_probs = result[0, top_classes] * 100

    razas = {}
    for i, class_idx in enumerate(top_classes):
        class_name = class_names[class_idx]
        prob = top_probs[i]
        print(f"{class_name}: {prob:.2f}%")
        razas[class_name] = float(round(prob,2))

    registro['imagen_razas']=razas
    print("------------------------------")
    print("dog breed clasification finish")
    print("------------------------------")

    return registro
