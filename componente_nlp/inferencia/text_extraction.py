import easyocr

# Reconocimiento de texto en imágenes (OCR)
ocr = easyocr.Reader(["es"])


def ExtractTextFromImage(registro):
    result = ocr.readtext(registro["imagen"])

    desc_img = []
    for r in result:
        desc_img.append(r[1] + " ")
    print("texto:", "".join(desc_img))
    registro["descripcion"] = "".join(desc_img)
    return registro
