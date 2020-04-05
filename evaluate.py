import cv2
import numpy as np
from PIL import Image
# 将ground truth和可视化图都二值化，计算Precision、Recall、MAE三种指标
def precision(groundtruthmask,visualizemask):
    visualizenum=0#可视化中白色像素点数量
    precisionnum=0#可视化中
    for x in range(visualizemask.shape[0]):
        for y in range(visualizemask.shape[1]):
            if visualizemask[x][y]==255:
                visualizenum+=1
                if groundtruthmask[x][y]==255:
                    precisionnum+=1
    print("precision:")
    print(visualizenum,precisionnum)
    print(precisionnum/visualizenum)

def recall(groundtruthmask,visualizemask):
    groundtruthnum=0
    recallnum=0
    for x in range(groundtruthmask.shape[0]):
        for y in range(groundtruthmask.shape[1]):
            if groundtruthmask[x][y]==255:
                groundtruthnum+=1
                if visualizemask[x][y]==255:
                    recallnum+=1
    print("recall:")
    print(groundtruthnum, recallnum)
    print(recallnum / groundtruthnum)

def MAE(groundtruthmask,visualizemask):
    sum=groundtruthmask.shape[0]*groundtruthmask.shape[1]
    maenum=0
    for x in range(groundtruthmask.shape[0]):
        for y in range(groundtruthmask.shape[1]):
            if groundtruthmask[x][y]!=visualizemask[x][y]:
                maenum+=1
    print("MAE:")
    print(sum, maenum)
    print(maenum / sum)

if __name__ == '__main__':
    imgname = "4 (17)"  # 图片名称

    groundtruthpath='groundtruth/'+imgname+'groundtruth' + '.png'
    groundtruthimg=cv2.imread(groundtruthpath,0)#读取groundtruth图片灰度图

    visualizemappath='result/'+imgname+'block4_unit3.png_0' + '.png'
    visualizeimg=cv2.imread(visualizemappath,0)#读取可视化图片灰度图

    ret,groundtruthmask=cv2.threshold(groundtruthimg,0,255,cv2.THRESH_OTSU)#OTSU阈值二值化,得到阈值和二值化图像
    ret, visualizemask = cv2.threshold(visualizeimg, 0, 255, cv2.THRESH_OTSU)  # OTSU阈值二值化

    precision(groundtruthmask,visualizemask)#计算查准率precision
    recall(groundtruthmask,visualizemask)#计算查全率recall
    MAE(groundtruthmask,visualizemask)

    groundtruthmask = Image.fromarray(groundtruthmask)
    groundtruthmask.save(imgname+'groundtruthmask.png')
    visualizemask = Image.fromarray(visualizemask)
    visualizemask.save(imgname + 'visualizemask.png')
