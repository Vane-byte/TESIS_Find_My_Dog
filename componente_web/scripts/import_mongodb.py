"""
Importa imágenes locales a la colección Raw_dogs (vacía la colección antes).
Ejecutar desde la raíz del repo: python -m componente_web.scripts.import_mongodb
"""
from glob import glob
from pathlib import Path

import pymongo

import config


def convert_to_document(dog_path: str, documents: list) -> None:
    print("perro", dog_path)
    with open(dog_path, "rb") as f:
        image_data = f.read()
    documents.append({"name": Path(dog_path).name, "data": image_data})


if __name__ == "__main__":
    img_fns = glob(config.RAW_DOGS_GLOB)
    documents: list = []
    for dog in img_fns:
        convert_to_document(dog, documents)

    client = pymongo.MongoClient(config.MONGO_URI)
    try:
        db = client[config.MONGO_DB_NAME]
        collection = db[config.MONGO_COLLECTION_RAW]
        collection.delete_many({})
        if documents:
            collection.insert_many(documents)
    finally:
        client.close()
