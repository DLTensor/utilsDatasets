import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('2012', 'train'), ('2012', 'val')]

# classes = ["Icon"]
classes = ["icon"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    # inFile = 'G:/Testin/100Classes/RICO_ICON/P20_2DIcon_Final/train/IconXMLtrain/'
    # in_file = open('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/xml/%s.xml' % image_id)
    # out_file = open('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/IconXML/IconLabeltrain/%s.txt' % image_id, 'w')
    in_file = open('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/xml/%s.xml' % image_id)
    out_file = open('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/IconXML/IconLabeltrain/%s.txt' % image_id, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        # if float(xmlbox.find('xmax').text) - float(xmlbox.find('xmin').text) < 32 and float(xmlbox.find('ymax').text) - float(xmlbox.find('ymin').text) < 32:
        #     continue
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def convert_annotation_Single(XMLName):
    # inFile = 'G:/Testin/100Classes/RICO_ICON/P20_2DIcon_Final/train/IconXMLtrain/'
    in_file = open(XMLName)
    out_file = open('out.txt', 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
if __name__ == '__main__':
    # image_ids = open('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/Icon_trainXML.txt').read().strip().split()
    # list_file = open('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/Icon_train721535.txt', 'w')
    image_ids = open('/home/liuyongkang/Icon100Images/FinalIconImg/IconXML/Icon_test.txt').read().strip().split()
    list_file = open('/home/liuyongkang/Icon100Images/FinalIconImg/IconXML/Icon_test5000.txt', 'w')
    for image_id in image_ids:
        print(image_id[:-4])
        # image_id = '000054c593aa4ec7bde5653175c1afc4_source.xml'
        # list_file.write('/home/liuyongkang/Icon100Images/FinalIconImg/genImg/img/%s.jpg\n' % image_id[:-4])
        list_file.write('/home/liuyongkang/Icon100Images/FinalIconImg/img/%s.jpg\n' % image_id[:-4])
        convert_annotation(image_id[:-4])
    list_file.close()
# wd = getcwd()
# for year, image_set in sets:
#     if not os.path.exists('../VOCdevkit/VOC%s/labels/'%(year)):
#         os.makedirs('../VOCdevkit/VOC%s/labels/'%(year))
#     image_ids = open('../VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
#     list_file = open('%s_%s.txt'%(year, image_set), 'w')
#     for image_id in image_ids:
#         list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
#         convert_annotation(year, image_id)
#     list_file.close()

