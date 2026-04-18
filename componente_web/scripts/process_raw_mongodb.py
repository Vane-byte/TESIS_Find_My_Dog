"""
Reclasifica documentos en Raw_dogs y escribe Hot_Dogs_Lost / Hot_Dogs_Found.
Ejecutar desde la raíz del repo: python -m componente_web.scripts.process_raw_mongodb
"""
import pymongo

import config
from componente_web.main_pipeline import buildPerritos


if __name__ == "__main__":
    client = pymongo.MongoClient(config.MONGO_URI)
    try:
        db = client[config.MONGO_DB_NAME]
        collection = db[config.MONGO_COLLECTION_RAW]
        hot_dogs_lost = db[config.MONGO_COLLECTION_HOT_LOST]
        hot_dogs_found = db[config.MONGO_COLLECTION_HOT_FOUND]

        hot_dogs_lost.delete_many({})
        hot_dogs_found.delete_many({})

        col = collection.find()
        lost_dogs, found_dogs = buildPerritos(col)

        if lost_dogs:
            hot_dogs_lost.insert_many(lost_dogs)
        if found_dogs:
            hot_dogs_found.insert_many(found_dogs)
    finally:
        client.close()
