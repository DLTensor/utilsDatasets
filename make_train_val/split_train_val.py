"""
code by lyk: 2020-11-24
indemind
function: split train val set

"""
import os
import random
import shutil

def split_train_val(image_path, xml_path, train_path, val_path, split_val_ratio):
    """

    :param image_path: images address
    :param xml_path: xmls address
    :param train_path: destination address
    :param val_path: validation address
    :param split_val_ratio: split rate
    :return:
    """

    xml_files = os.listdir(xml_path)
    nums = len(xml_files)
    print(xml_files[:20])
    random.shuffle(xml_files)
    print(xml_files[:20])
    if not os.path.exists(val_path):
        os.mkdir(val_path)
    if not os.path.exists(train_path):
        os.mkdir(train_path)
    for index, xml_file in enumerate(xml_files):
        name, ext_tail = os.path.splitext(xml_file)
        xml_file_path = os.path.join(xml_path, xml_file)
        image_file_path = os.path.join(image_path, name + '.png')
        if index < (nums * split_val_ratio):
            des_img_path = os.path.join(val_path, name + '.png')
            des_xml_path = os.path.join(val_path, xml_file)
            print(index, name, xml_file_path, image_file_path, ext_tail)
            shutil.copy(image_file_path, des_img_path)
            shutil.copy(xml_file_path, des_xml_path)
        else:
            des_img_path = os.path.join(train_path, name + '.png')
            des_xml_path = os.path.join(train_path, xml_file)
            print(index, name, xml_file_path, image_file_path, ext_tail)
            shutil.copy(image_file_path, des_img_path)
            shutil.copy(xml_file_path, des_xml_path)


if __name__ == '__main__':
    src_img_path = "D:/00_indemind_lyk/dataset/officeAround/allneed2/allneed2/image"
    src_xml_path = "D:/00_indemind_lyk/dataset/officeAround/allneed2/allneed2/xml"
    train_img_path = "D:/00_indemind_lyk/dataset/officeAround/allneed2/allneed2/train"
    val_img_path = "D:/00_indemind_lyk/dataset/officeAround/allneed2/allneed2/val"
    rate_split = 0.1
    split_train_val(src_img_path, src_xml_path, train_img_path, val_img_path, rate_split)