import os
import utils

imgList = []
with open('Icon_train.txt', 'r') as fileIcon:
    Icon_list = fileIcon.readlines()

    for imgpath in Icon_list:
        imgList.append(imgpath.strip())

nums = 0
for img in imgList:
    # os.remove(img)
    print(img)
    nums +=1
print(nums)



