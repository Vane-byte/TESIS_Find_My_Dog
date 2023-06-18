import tensorflow
from keras.models import load_model
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.preprocessing.image import load_img 
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

import numpy as np

new_model = load_model(r'D:\Mis documentos\Documents\CLASES\tesiss\Codigo\ALL\Helpers\Modelos\RESENTV2.h5')
IMG_SIZE = 299
INIT_LR = 1e-5
EPOCHS =  20
BS = 32
class_names = ['n02086240-Shih-Tzu',
               'n02086079-Pekinese',
               'n02097209-standard_schnauzer',
               'n02097047-miniature_schnauzer',
               'n02102318-cocker_spaniel',
               'n02110958-pug',
               'n02088364-beagle',
               'n02085620-Chihuahua',
               'n02099601-golden_retriever'
               'n02112018-Pomeranian',
               'n02108089-boxer',
               'n02110185-Siberian_husky',
               'n02113624-toy_poodle',
               'n02106550-Rottweiler',
               'n02108915-French_bulldog',
               'n02113712-miniature_poodle',
               'n02107142-Doberman',
               'n02099712-Labrador_retriever',
               'n02093256-Staffordshire_bullterrier',
               'n02096585-Boston_bull',
               'n02097474-Tibetan_terrier',
               'n02102177-Welsh_springer_spaniel',
               'n02087046-toy_terrier',
               'n02095314-wire-haired_fox_terrier',
               'n02106166-Border_collie',
               'n02089867-Walker_hound',
               'n02101388-Brittany_spaniel',
               'n02106662-German_shepherd',
               'n02094433-Yorkshire_terrier',
               'n02093428-American_Staffordshire_terrier',
               'n02085936-Maltese_dog',]

from PIL import Image,ImageDraw
def predimage(path):
    image = Image.open(path)
    test = load_img(path,target_size=(299,299))
    test = img_to_array(test)
    test = np.expand_dims(test,axis=0)
    test /= 255 
    result = new_model.predict(test,batch_size = BS)
    y_class = result.argmax(axis=-1)
    result = (result*100)
    result = list(np.around(np.array(result),2))
    i = y_class[0]
    s = result[0][i]
    plt.text(0, 0,class_names[y_class[0]],size=12,color='purple')
    plt.text(0, 50,s,size=15,color='red')
    plt.imshow(image)
    print(result)
    print(class_names[y_class[0]])


#predimage('C:/Users/W10/Desktop/TEST2.jpg',class_names)