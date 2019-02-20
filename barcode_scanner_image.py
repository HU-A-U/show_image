import numpy as np
import cv2

def detect(image):
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 15))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    # find the contours in the thresholded image
    (_,cnts,_) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # if no contours were found, return None
    if len(cnts) == 0:
        return None

    # otherwise, sort the contours by area and compute the rotated
    # bounding box of the largest contour
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    bb = box.tolist()
    x = 9999999999999
    y = 9999999999999
    h = 0
    w = 0
    for p in bb:
        if p[0]<x:
            x = p[0]
        elif p[1]<y:
            y = p[1]

        if p[1] > h:
            h = p[1]
        elif p[0]>w:
            w = p[0]

    # 展示输出图像
    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    cv2.imwrite("final1.jpg", image)

    return (x-20,y-20,w+20,h+20)


if __name__ == '__main__':

    # 加载输入图像
    image1 = cv2.imread('789.jpg')
    from PIL import Image
    img = Image.open('789.jpg')
    box = detect(image1)
    cropped = img.crop(box)
    print(type(cropped))
    width = cropped.size[0]
    height = cropped.size[1]
    bs = 1
    new_img = cropped.resize((width*bs, height*bs),Image.ANTIALIAS)

    new_img.show()

