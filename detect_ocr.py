import os
import torch
import easyocr
import re
import cv2 as cv

from region_mapping import region_mapping


def detect_dash(input_text: str):
    pattern = re.compile(r".*-")
    return pattern.match(input_text)


def detect_alphabet(input_text: str):
    pattern = re.compile(r"\d\d[a-zA-Z]")
    return pattern.match(input_text)


print(torch.cuda.is_available())
# Model
# or yolov5n - yolov5x6, custom
model = torch.hub.load(
    "ultralytics/yolov5",
    model="custom",
    source="github",
    path="./license_4146_50.pt",
)

# Images
# or file, Path, PIL, OpenCV, numpy, list
# img = 'https://ultralytics.com/images/zidane.jpg'
pathToTestImage = "./license/test/"
pathToDetectImage = "./runs/detect/exp/crops/license/"

imgs = [pathToTestImage + file for file in os.listdir(pathToTestImage)]
model.iou = 0.1
results = model(imgs)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# results.show()
results.crop(save=True)
# increase crop size

df = [result for result in results.pandas().xyxy]
print(df[0])
print(df[0].confidence)

reader = easyocr.Reader(["vi"])
for fileName in os.listdir(pathToDetectImage):
    result = reader.readtext(pathToDetectImage + fileName)
    print(f"file name {fileName}")
    print(f"size {len(result)}")
    for i in range(len(result)):
        print(f"{i} : {result[i][1]}")
        if detect_dash(result[i][1]) or detect_alphabet(result[i][1]):
            region_line = result[i][1][0:2]
            # use region mapping dictionary
            try:
                print(f"region : {region_mapping[region_line]}")
            except KeyError:
                print("region not found")
