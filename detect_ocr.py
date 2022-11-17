import os
import torch
import easyocr
import torch
print(torch.cuda.is_available())
# Model
# or yolov5n - yolov5x6, custom
model = torch.hub.load(
    'ultralytics/yolov5', model='custom',  source='github', path='./license_2202.pt')

# Images
# or file, Path, PIL, OpenCV, numpy, list
# img = 'https://ultralytics.com/images/zidane.jpg'
pathToTestImage = './license/test/'
pathToDetectImage = './runs/detect/exp/crops/license/'
imgs = [pathToTestImage +
        file for file in os.listdir(pathToTestImage)]
model.iou = 0.1
results = model(imgs)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# results.show()
results.crop(save=True)
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
