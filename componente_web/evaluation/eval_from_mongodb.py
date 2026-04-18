import pymongo
import pandas as pd

import config
from componente_web.evaluation.register_evaluation import calTotal
from componente_web.main_pipeline import processPerritos


def finalEvaluation(registro):
    client = pymongo.MongoClient(config.MONGO_URI)
    try:
        db = client[config.MONGO_DB_NAME]
        perrito = processPerritos(registro)

        if perrito["SePerdio"] == 1:
            perrito["SePerdio"] = "Perro Perdido"
            all_regs = db[config.MONGO_COLLECTION_HOT_FOUND].find()
        else:
            perrito["SePerdio"] = "Perro Encontrado"
            all_regs = db[config.MONGO_COLLECTION_HOT_LOST].find()

        updated_regs = calTotal(list(all_regs), perrito)
        df = pd.DataFrame(updated_regs)
        df = df.sort_values(by=["Total"], ascending=False)
        df = df.head(10)
        dict_list = df.to_dict("records")

        print(df[["name", "NER_points", "IMG_points"]])
        print("NER: ", perrito["NER"], "\nRazas: ", perrito["imagen_razas"])
        return perrito, dict_list
    finally:
        client.close()
