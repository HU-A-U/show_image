# import pyzbar.pyzbar as pyzbar
# from PIL import Image,ImageEnhance,ImageDraw
# import cv2
#
#
# # img = Image.open('11.jpg')
# #
# # img = ImageEnhance.Brightness(img).enhance(2.0)#增加亮度
# #
# # img = ImageEnhance.Sharpness(img).enhance(17.0)#锐利化
# #
# # img = ImageEnhance.Contrast(img).enhance(4.0)#增加对比度
# #
# # img = img.convert('L')#灰度化
# #
# # img.show()
# #
# # barcodes = pyzbar.decode(img)
# #
# # for barcode in barcodes:
# #     barcodeData = barcode.data.decode('utf-8')
# #
# #     print(barcodeData)
#
#
# def decodeDisplay(img_path):
#     img = Image.open(img_path)
#     barcodes = pyzbar.decode(img)
#     for barcode in barcodes:
#         # 提取二维码的边界框的位置
#         # 画出图像中条形码的边界框
#         (x, y, w, h) = barcode.rect
#         draw = ImageDraw.Draw(img)
#         draw.line([x,y],fill=(0, 0, 255))
#         img.show()
#
#     return img
#
# if __name__ == '__main__':
#     # decodeDisplay('11.jpg')
#     decodeDisplay('11.png')

import numpy as np
import argparse
import cv2


image = cv2.imread('11.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

cv2.imshow("gradient",gradient)
#原本没有过滤颜色通道的时候，这个高斯模糊有效，但是如果进行了颜色过滤，不用高斯模糊效果更好
#blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(gradient, 225, 255, cv2.THRESH_BINARY)
cv2.imshow("thresh",thresh)
cv2.imwrite('thresh.jpg',thresh)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow("closed",closed)
cv2.imwrite('closed.jpg',closed)

closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)
cv2.imwrite('closed1.jpg',closed)

img,cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))

cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imwrite("final.jpg",image)
cv2.imshow("Image", image)

cv2.waitKey(0)
