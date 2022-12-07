import pytesseract


def getTextFromImage(image):
    try:
        return pytesseract.image_to_string(image, config='--psm 12')
    except:
        print("Could not convert image")


# print(getTextFromImage('./license/test/21.jpg'))
