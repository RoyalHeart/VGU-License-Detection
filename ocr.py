import easyocr

reader = easyocr.Reader(["vi"])


def getTextFromImage(img):
    return reader.readtext(img)
