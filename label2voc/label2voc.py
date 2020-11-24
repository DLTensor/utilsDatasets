from xml.dom import minidom
import json
import glob
import os
from shutil import copyfile
# 将self.orderDict中的信息写入本地xml文件，参数filename是xml文件名
names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush']

def Convert_label_to_voc(labelFile,JPEGImage_path,out_path):
    '''
    将coco数据转换为voc数据
    :param labelFile:label文件名称
    :param JPEGImage_path: 图片数据集的位置
    :param out_path: 生成的voc数据集保存的位置
    :return:
    '''
    #先创建voc输出文件夹标准格式
    outdir = out_path
    # # 创建各级文件夹
    # train_xml_out = os.path.join(outdir, 'VOC2007/Annotations')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # train_img_out = os.path.join(outdir, 'VOC2007/JPEGImages')
    # if not os.path.exists(train_img_out):
    #     os.makedirs(train_img_out)
    # filepath, tmpfilename = os.path.split(fileUrl)
    # shotname, extension = os.path.splitext(tmpfilename)

    _, filename = os.path.split(labelFile)
    filename = filename.split('.')[0] + '.png'
    print(filename)
    img_w = 640
    img_h = 400
    data = open(labelFile, 'r')
    roi_list = list()
    lines = data.readlines()
    for line in lines:
        classindex, x1, y1, x2, y2 = line.strip().split()
        print(classindex, x1, y1, x2, y2)
        tmp_box=[float(x1), float(y1), float(x2), float(y2)]
        box = convert_boxshape((img_w, img_h), tmp_box)
        roi_list.append([names[int(classindex)], box[0], box[1], box[2], box[3]])
        print(box)
    get_xml(filename, [img_w, img_h, 3], roi_list, outdir)

def convert_boxshape(size, box):
    '''
    coco数据集标注是xmin,ymin,width,height 而voc和yolo是xmin ymin xmax ynax 需要进行转换
    :param size: 图片宽 图片高
    :param box:
    :return:
    '''
    dw = size[0]   # 图像实际宽度
    dh = size[1]  # 图像实际高度

    x1 = box[0]  #标注区域X坐标
    y1 = box[1]  #标注区域Y坐标
    x2 = box[2]  # 标注区域宽度
    y2 = box[3]  #标注区域高度

    xmin=int(x1)
    ymin=int(y1)
    xmax=int(x2)
    ymax=int(y2)
    return (xmin, ymin, xmax, ymax)


def get_xml(img_name,size,roi,outpath):
    '''
    传入每张图片的名称 大小 和标记点列表生成和图片名相同的xml标记文件
    :param img_name: 图片名称
    :param size:[width,height,depth]
    :param roi:[["label1",xmin,ymin,xmax,ymax]["label2",xmin,ymin,xmax,ymax].....]
    :return:
    '''
    impl = minidom.getDOMImplementation()
    doc = impl.createDocument(None, None, None)
    #创建根节点
    orderlist = doc.createElement("annotation")
    doc.appendChild(orderlist)
    #c创建二级节点
    filename=doc.createElement("filename")
    filename.appendChild(doc.createTextNode(img_name))
    orderlist.appendChild(filename)
    #size节点
    sizes=doc.createElement("size")
    width=doc.createElement("width")
    width.appendChild(doc.createTextNode(str(size[0])))
    height=doc.createElement("height")
    height.appendChild(doc.createTextNode(str(size[1])))
    depth=doc.createElement("depth")
    depth.appendChild(doc.createTextNode(str(size[2])))
    sizes.appendChild(width)
    sizes.appendChild(height)
    sizes.appendChild(depth)
    orderlist.appendChild(sizes)
    #object 节点
    for ri in roi:
        object=doc.createElement("object")
        name=doc.createElement("name")
        name.appendChild(doc.createTextNode(ri[0]))
        object.appendChild(name)
        bndbox=doc.createElement("bndbox")

        xmin=doc.createElement("xmin")
        xmin.appendChild(doc.createTextNode(str(ri[1])))
        bndbox.appendChild(xmin)
        ymin=doc.createElement("ymin")
        ymin.appendChild(doc.createTextNode(str(ri[2])))
        bndbox.appendChild(ymin)
        xmax=doc.createElement("xmax")
        xmax.appendChild(doc.createTextNode(str(ri[3])))
        bndbox.appendChild(xmax)
        ymax=doc.createElement("ymax")
        ymax.appendChild(doc.createTextNode(str(ri[4])))
        bndbox.appendChild(ymax)
        object.appendChild(bndbox)
        orderlist.appendChild(object)
         # 将dom对象写入本地xml文件

    # 打开test.xml文件 准备写入
    f = open(os.path.join(outpath,img_name[:-4]+'.xml'), 'w')
    # 写入文件
    doc.writexml(f, addindent='  ', newl='\n')
    # 关闭
    f.close()

if __name__ == "__main__":
    #传入coco的annotations.json地址，image文件存放的地址 和输出的voc数据存放地址
    # Convert_coco_to_voc("json address", "image dir", "voc label dir")
    dirpath = "D:/00_indemind_lyk/dataset/officeAround/imu_camera/imu_camera/output"

    txtFiles = glob.glob(os.path.join(dirpath, '*.txt'))
    print(txtFiles)
    for txtfile in txtFiles:
        Convert_label_to_voc(txtfile, "D:/00_indemind_lyk/dataset/officeAround/imu_camera/imu_camera/allimg", "D:/00_indemind_lyk/dataset/officeAround/imu_camera/imu_camera/xml")

