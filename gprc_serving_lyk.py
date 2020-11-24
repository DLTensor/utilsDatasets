# -*- coding: utf-8 -*-

import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

SERVER_URL = "10.32.25.190:8099"

class_names = ['forward']
#SERVER_URL = "10.32.25.207:9091"

def transfer_to_xywh_box(width, height, box):
    ymin, xmin, ymax, xmax = box
    xmin = float(xmin * width)
    ymin = float(ymin * height)
    xmax = float(xmax * width)
    ymax = float(ymax * height)
    return xmin, ymin, xmax - xmin, ymax - ymin

def letterbox_image(image, size):
    """
    Introduction
    ------------
        对预测输入图像进行缩放，按照长宽比进行缩放，不足的地方进行填充
    Parameters
    ----------
        image: 输入图像
        size: 图像大小
    Returns
    -------
        boxed_image: 缩放后的图像
    """
    image_w, image_h = image.size
    w, h = size
    new_w = int(image_w * min(w*1.0/image_w, h*1.0/image_h))
    new_h = int(image_h * min(w*1.0/image_w, h*1.0/image_h))
    resized_image = image.resize((new_w,new_h), Image.BICUBIC)

    boxed_image = Image.new('RGB', size, (128, 128, 128))
    boxed_image.paste(resized_image, ((w-new_w)//2,(h-new_h)//2))
    return boxed_image
def get_grpc(image_path):
    channel = grpc.insecure_channel(SERVER_URL)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    # Send request
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'findforward'
    request.model_spec.signature_name = 'predict_images'

    image = Image.open(image_path)
    resize_image = letterbox_image(image, (416, 416))
    image_data = np.array(resize_image, dtype=np.float32)
    image_data /= 255.
    image_data = np.expand_dims(image_data, axis=0)
    request.inputs['images'].CopyFrom(tf.make_tensor_proto(image_data))
    request.inputs['imghw'].CopyFrom(tf.make_tensor_proto([image.size[1], image.size[0]]))

    result = stub.Predict(request, 100.0)  # 10 secs timeout

    #image_height, image_width, _ = image.shape
    scores = result.outputs["scores"].float_val
    boxes = result.outputs['Boxes'].float_val
    # Classes = result.outputs['Classes'].float_val
    boxes = np.reshape(boxes, [-1, 4])
    count = 0
    data = []
    for i in range(len(scores)):
        score = scores[i]
        if score > 0.7:
            box = boxes[i]
            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            a = (score, left, top, right, bottom)
            data.append(list(a))
            count = count + 1

    if count == 0:
        return {"author": "刘永康", "code": 0, "msg": "not find", "modelname": "findforward", "predict": ""}
    else:
        return {"author": "刘永康", "code": 1, "msg": "success", "modelname": "findforward",
                "predict": {"data": data, "icon": "forward", "num": count}}


if __name__ == '__main__':
    import time

    a = time.time()
    print(get_grpc("/home/liuyongkang/tensorflow-yolo3/Icon_data/test2_1/0001018.png"))
    print(time.time() - a)
