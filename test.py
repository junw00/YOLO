import os
import glob
from ultralytics import YOLO

test_images = glob.glob(os.path.join('./test/images') + '\*.jpg')

model = YOLO('./best.pt')

for test_image in test_images:
    model(test_image, save=True)
