from xml.dom import minidom
import json
import glob
import os
from shutil import copyfile
import cv2
import xml.etree.ElementTree as ET


names=['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush']
classes = {'person': 0}

if __name__ == "__main__":
    xmlpath = "D:/00_indemind_lyk/dataset/officeAround/cam0/xml"
    # imageDir = "D:/00_indemind_lyk/dataset/officeAround/cam0/dataframe"
    imageDir = "D:/00_indemind_lyk/dataset/officeAround/allNeed/image"
    xmlpath2 = "D:/00_indemind_lyk/dataset/officeAround/allNeed/xml"

    xmlFiles = glob.glob(os.path.join(xmlpath2, '*.xml'))
    print(xmlFiles)
    for xml in xmlFiles:
        _, name = os.path.split(xml)
        xml = os.path.join(xmlpath2, name)
        in_file = open(xml, "r")

        tree = ET.parse(in_file)
        root = tree.getroot()
        imagename = root.find('filename')
        imagepath = os.path.join(imageDir, imagename.text)
        image = cv2.imread(imagepath)



        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes[cls]
            xmlbox = obj.find('bndbox')
            # if float(xmlbox.find('xmax').text) - float(xmlbox.find('xmin').text) < 32 and float(xmlbox.find('ymax').text) - float(xmlbox.find('ymin').text) < 32:
            #     continue
            b = [int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text), int(xmlbox.find('ymax').text)]
            cv2.rectangle(image, (b[0], b[2]), (b[1], b[3]), (0, 255, 0))
        cv2.imshow('imag', image)
        cv2.waitKey()
