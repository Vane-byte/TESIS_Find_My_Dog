"""
Orquestación del pipeline de un registro (OCR → clasificación → NER → visión).

Los imports de NLP y visión son **perezosos** para que procesos que solo usan parte del
stack (p. ej. tests del web sin TF) no carguen modelos hasta llamar a `processPerritos`.
Para ejecución totalmente separada por servicio, el siguiente paso sería sustituir
estas llamadas por peticiones HTTP a APIs del componente NLP y del componente visión.
"""


def processPerritos(registro):
    from componente_nlp.inferencia.ner import PredictNER
    from componente_nlp.inferencia.text_classification import DogStateClasification
    from componente_nlp.inferencia.text_extraction import ExtractTextFromImage
    from componente_vision.inferencia.image_classification import recognitionDog

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
