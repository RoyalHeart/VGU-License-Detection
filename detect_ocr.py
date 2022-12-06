from module.region_mapping import getRegionNoAccents
from module.timing import timing
import module.regular_expression as re
import module.ocr as ocr
import cv2
import torch
import os
import time
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
modelSmall = torch.hub.load(
    "ultralytics/yolov5",
    model="custom",
    source="github",
    path="./license_4146_50_s.pt",
)
modelMedium = torch.hub.load(
    "ultralytics/yolov5",
    model="custom",
    source="github",
    path="./license_4146_50_m.pt",
)
modelLarge = torch.hub.load(
    "ultralytics/yolov5",
    model="custom",
    source="github",
    path="./license_4146_50_l.pt",
)


def putTextOnFrame(frame, text, x, y):
    cv2.putText(frame,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (36, 255, 12),
                2,)
    return frame


def saveImage(image, filename):
    cv2.imwrite(filename, image)


def regionMappingFrame(ocrResults, frame, xmin, ymin):
    for i in range(len(ocrResults)):
        # print(f"{i} : {result[i][1]}")
        ocrText = ocrResults[i][1]
        if re.detect_dash(ocrText) or re.detect_alphabet(ocrText):
            region_number = ocrText[0:2]
            try:
                region = getRegionNoAccents(region_number)
                frame = putTextOnFrame(frame, region, xmin, ymin)
            except KeyError:
                print("region not found")


def showLicenseRegionOnFrame(results, frame: np.ndarray, filename=None, isShow=True):
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
    if (filename):
        print("Save file")
        print(filename)
        cv2.imwrite(filename, cv2.cvtColor(
            edited_frame, cv2.COLOR_BGR2RGB))
    if (isShow):
        cv2.imshow("edited frame", edited_frame)


def detect_ocr_video(vidcap, modelType='small', frameRate=30):
    success, frame = vidcap.read()
    count = 0
    prev = 0
    model = modelSmall
    if (modelType == 'small'):
        model = modelSmall
        print("small")
    elif (modelType == 'medium'):
        model = modelMedium
        print("medium")
    elif (modelType == 'large'):
        model = modelLarge
        print("large")
    while success:
        time_elapsed = time.time() - prev
        success, frame = vidcap.read()
        if time_elapsed > 1./frameRate:
            prev = time.time()
            count += 1
            model.iou = 0.1
            results = model(frame)
            timing(showLicenseRegionOnFrame, results, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def detect_ocr_image(pathToImage, modelType: str = 'small', savePath=None):
    image = cv2.cvtColor(cv2.imread(
        pathToImage), cv2.COLOR_BGR2RGB)
    model = modelSmall
    if (modelType == 'small'):
        model = modelSmall
    elif (modelType == 'medium'):
        model = modelMedium
    elif (modelType == 'large'):
        model = modelLarge
    else:
        return Exception
    results = model(image)
    model.iou = 0.1
    filename = None
    if (savePath):
        filename = f'{savePath}detected_{modelType}_{os.path.basename(pathToImage)}'
    print(filename)
    showLicenseRegionOnFrame(results, image, filename, False)


def detectLicense(dir):
    imgs = []
    for i in os.listdir(dir):
        imgs.append(dir + i)
    results = modelSmall(imgs)
    results.save()
    return results


def main():
    username = "hoangtam"
    password = "vgulicensedetection"
    port = "172.16.129.39:8080"
    ipCameraAddress = f"https://{username}:{password}@{port}/video"
    video_path = "./OUTFILE.mp4"
    # vidcap = cv2.VideoCapture(ipCameraAddress)
    vidcap = cv2.VideoCapture(video_path)
    # vidcap = cv2.VideoCapture(0)
    # timing(detectLicense, "./license/test/")
    print('hi')
    # detect_ocr_video(vidcap, 'medium', 10)
    detect_ocr_image("./upload_file/03.jpg", 'medium', './static/medium/')
    # Exit and distroy all windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
