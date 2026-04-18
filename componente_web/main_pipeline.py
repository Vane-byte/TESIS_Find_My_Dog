from componente_nlp.inferencia.ner import PredictNER
from componente_nlp.inferencia.text_classification import DogStateClasification
from componente_nlp.inferencia.text_extraction import ExtractTextFromImage
from componente_vision.inferencia.image_classification import recognitionDog


def processPerritos(registro):
    if registro["descripcion"] == "":
        registro = ExtractTextFromImage(registro)

    print("Inicio de clasificación de publicación ")
    print("_______________________________________")
    registro = DogStateClasification(registro)

    print("Inicio de reconocimiento de atributos ")
    print("_______________________________________")
    registro = PredictNER(registro)

    print("Inicio de reconocimiento de raza ")
    print("_______________________________________")
    registro = recognitionDog(registro)
    return registro


def buildPerritos(collection):
    lost_dogs = []
    found_dogs = []
    for dog in collection:
        registro = {
            "descripcion": "",
            "imagen": dog["data"],
            "name": dog["name"],
        }
        perrito = processPerritos(registro)
        if perrito["SePerdio"] == 1:
            lost_dogs.append(perrito)
        else:
            found_dogs.append(perrito)

    return lost_dogs, found_dogs
