import numpy as np
from PIL import Image
import cv2
# 扫描图像，寻找红框，并生成ground truth图像

def markBox(array, img):
    # 方框左上角和右下角坐标初始化
    minX = minY =  0
    maxX = maxY = 223
    # 按行扫描
    label = True  # True表示扫描第一条边，False表示扫描第二条边
    num = 0  # 计数，连续红色像素点的个数
    for row in range(img.shape[0]):  # 图片的高，多少行
        if num >= 10 and label == False:  # 第二条边已经记录，跳出
            break
        for col in range(img.shape[1]):  # 图片的宽，多少列
            pixel = img[col, row]  # 获取像素点
            # print(row,col)
            if (pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 120):  # 如果是红色，bgr值
                num += 1
                if num >= 40:  # 连续红色30像素
                    if label:  # 是第一条边
                        minY = row
                        label = False
                        num = 0
                        break
                    else:  # 是第二条边
                        maxY = row
                        break
            else:
                num = 0
    # 按列扫描
    label = True  # True表示扫描第一条边，False表示扫描第二条边
    num = 0
    for col in range(img.shape[1]):  # 图片的宽，多少列
        if num >= 10 and label == False:
            break
        for row in range(img.shape[0]):  # 图片的高，多少行
            pixel = img[col, row]
            if (pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 120):
                num += 1
                if num >= 40:
                    if label:
                        minX = col
                        num = 0
                        label = False
                        break
                    else:
                        maxX = col
                        break
            else:
                num = 0
    print(minX, minY, maxX, maxY)

    #修改数组，改变灰度
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            array[x, y] += 25.5

    # print(array)
    return array


if __name__ == '__main__':
    array = np.ones((224, 224)) * 0#初始化矩阵，即图像像素大小
    imgname="4 (17)"#图片名称
    for i in range(1, 11):#循环处理10张标记图片,最好用png格式，框线更清楚
        imgpath = 'images/'+imgname+'_' + str(i) + '.jpg'
        img = cv2.imread(imgpath)
        array = markBox(array, img)

    groundtruth = Image.fromarray(array)
    groundtruth=groundtruth.convert('L')#矩阵转为灰度图
    groundtruth.save(imgname+'groundtruth.png')
