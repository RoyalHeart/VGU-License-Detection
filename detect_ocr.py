from region_mapping import getRegionNoAccents
from timing import timing
import regular_expression as re
import cv2
import torch
import ocr
import os
import pandas as pd
import numpy as np
# import argparse
# parser = argparse.ArgumentParser()

# # -db DATABSE -u USERNAME -p PASSWORD -size 20
# parser.add_argument(
#     "-i", "--input", help="Type of input 0: camera, 1: ipCamera, 2: image/video source", type=int)

# args = parser.parse_args()

# print("Input {}".format(
#     args.input | 0,
# ))

print(cv2.__version__)
print(torch.cuda.is_available())
# Model
# or yolov5n - yolov5x6, custom
model = torch.hub.load(
    "ultralytics/yolov5",
    model="custom",
    source="github",
    path="./license_4146_50_l.pt",
)


def regionMappingFrame(ocrResults, frame, xmin, ymin):
    for i in range(len(ocrResults)):
        # print(f"{i} : {result[i][1]}")
        ocrText = ocrResults[i][1]
        if re.detect_dash(ocrText) or re.detect_alphabet(ocrText):
            region_number = ocrText[0:2]
            try:
                region = getRegionNoAccents(region_number)
                cv2.putText(
                    frame,
                    region,
                    (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )
            except KeyError:
                print("region not found")


def showLicenseRegionOnFrame(results, frame: np.ndarray):
    # print(type(frame))
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
                edited_frame = cv2.rectangle(
                    edited_frame, (xmin, ymin), (xmax, ymax), (36, 255, 12), 1
                )
                ocrResults = ocr.getTextFromImage(license_crop)
                regionMappingFrame(
                    ocrResults, edited_frame, xmin, ymin)
            except:
                print("Type error")
    cv2.imshow("edited frame", edited_frame)


def detect_ocr_video(vidcap):
    success, frame = vidcap.read()
    count = 0
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        success, frame = vidcap.read()
        count += 1
        model.iou = 0.1
        results = model(frame)
        showLicenseRegionOnFrame(results, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def detect_ocr_image(image):
    results = model(image)
    model.iou = 0.1
    showLicenseRegionOnFrame(results, image)


# username = "hoangtam"
# password = "vgulicensedetection"
# port = "172.16.128.209:8080"
# ipCameraAddress = f"https://{username}:{password}@{port}/video"
# vidcap = cv2.VideoCapture(ipCameraAddress)
video_path = "./OUTFILE.mp4"
vidcap = cv2.VideoCapture(video_path)
# vidcap = cv2.VideoCapture(0)


def detectLicense(dir):
    imgs = []
    for i in os.listdir(dir):
        imgs.append(dir + i)
    results = model(imgs)
    results.save()
    return results


def main():
    timing(detectLicense, "./license/validation/")
    # detect_ocr_video(vidcap)
    # detect_ocr_image(cv2.cvtColor(cv2.imread(
    # "./license/test/24.jpg"), cv2.COLOR_BGR2RGB))
    # Exit and distroy all windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
