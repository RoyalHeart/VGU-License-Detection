import matplotlib.pyplot as plt
import cv2
import os
import torch
import easyocr
import re
import pandas as pd

from region_mapping import region_mapping_no_accents as region_mapping


def detect_dash(input_text: str):
    pattern = re.compile(r".*-")
    return pattern.match(input_text)


def detect_alphabet(input_text: str):
    pattern = re.compile(r"\d\d[a-zA-Z]")
    return pattern.match(input_text)


print(cv2.__version__)
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
# pathToTestImage = './license/test/'
# pathToDetectImage = './runs/detect/exp/crops/license/'
# imgs = [pathToTestImage +
#         file for file in os.listdir(pathToTestImage)]

reader = easyocr.Reader(["vi"])


def showLicenseOnFrame(results, frame):
    df = results.pandas().xyxy
    edited_frame = frame
    if not (df[0].empty):
        licenses = df[0]
        for i in range(len(licenses.xmin)):
            try:
                ymin = round(float(pd.to_numeric(licenses.ymin[i])))
                ymax = round(float(pd.to_numeric(licenses.ymax[i])))
                xmin = round(float(pd.to_numeric(licenses.xmin[i])))
                xmax = round(float(pd.to_numeric(licenses.xmax[i])))
                license_crop = frame[ymin:ymax, xmin:xmax]
                result = reader.readtext(license_crop)
                edited_frame = cv2.rectangle(
                    edited_frame, (xmin, ymin), (xmax, ymax), (36, 255, 12), 1
                )
                for i in range(len(result)):
                    print(f"{i} : {result[i][1]}")
                    if detect_dash(result[i][1]) or detect_alphabet(result[i][1]):
                        region_line = result[i][1][0:2]
                        # use region mapping dictionary
                        try:
                            cv2.putText(
                                edited_frame,
                                region_mapping[region_line],
                                (xmin, ymin - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                (36, 255, 12),
                                2,
                            )
                            print(f"region : {region_mapping[region_line]}")
                        except KeyError:
                            print("region not found")
            except:
                print("Type error")
        cv2.imshow("edited frame", edited_frame)


username = "hoangtam"
password = "vgulicensedetection"
port = "192.168.1.3:8080"
vidcap = cv2.VideoCapture(f"https://{username}:{password}@{port}/video")
video_path = "./OUTFILE.mp4"
# vidcap = cv2.VideoCapture(0)
success, frame = vidcap.read()
count = 0
while True:
    vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
    success, frame = vidcap.read()
    count += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    model.iou = 0.1
    results = model(frame)
    showLicenseOnFrame(results, frame)

# Exit and distroy all windows
cv2.destroyAllWindows()

# # Results
# model.iou = 0.1
# results = model("./license/test/21.jpg")
# results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# # results.show()
# # results.crop(save=True)
# # increase crop size

# df = results.pandas().xyxy
# print(len(df[0].xmin))
# print(df[0].confidence)

# reader = easyocr.Reader(["vi"])
# for fileName in os.listdir(pathToDetectImage):
#     result = reader.readtext(pathToDetectImage + fileName)
#     print(f"file name {fileName}")
#     print(f"size {len(result)}")
#     for i in range(len(result)):
#         print(f"{i} : {result[i][1]}")
#         if detect_dash(result[i][1]) or detect_alphabet(result[i][1]):
#             region_line = result[i][1][0:2]
#             # use region mapping dictionary
#             try:
#                 print(f"region : {region_mapping[region_line]}")
#             except KeyError:
#                 print("region not found")
