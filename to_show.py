# -*- coding:utf-8 -*-
import base64
import time
import cv2
import requests
import numpy as np
from PIL import Image
from flask import Flask
from flask import request
from io import BytesIO,StringIO
from config import Config
from splinter import Browser
from barcode_scanner_image import detect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
# 配置
app.config.from_object(Config)
browser = Browser('chrome')
browser.driver.maximize_window()
wait = WebDriverWait(browser.driver, 60)
@app.route('/showimg', methods=['GET', 'POST'])
def showimg():
    # 获取到图片url
    data = request.json or {}
    res = {}
    img_path = ''
    rate = 2
    if not data:
        if not request.form:
            res['msg'] = '没有数据'
        else:
            img_path = request.form.get('img_path', '')
            rate = request.form.get('rate', '')
    else:
        img_path = request.json.get('img_path', '')
        rate = request.json.get('rate', '')

    # 下载图片
    target_img = requests.get(img_path).content
    target_array = np.fromstring(target_img, np.uint8)  # 转换np序列
    image = cv2.imdecode(target_array, cv2.IMREAD_COLOR)  # 转换Opencv格式
    PIL_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) # 转换PIL.Image格式
    #进行二维码识别
    box = detect(image)

    #按照图片的比率进行缩放,返回base64格式
    base64_str = zoom(PIL_image,rate,box)

    html_str = '''<div id='show_img' style='text-align: center;margin-top: 200px;'><img style='transform:scale({0});-ms-transform:scale({0});-webkit-transform:scale({0});-o-transform:scale({0});-moz-transform:scale({0});' src='data:image/png;base64,{1}'/></div>'''.format(rate,base64_str)

    # from tasks import _toShow
    # status = _toShow.delay(img_path)
    for i in range(3):
        try:
            status = _toShow(html_str)
        except Exception as e:
            print(e)
        if status[1] == 200:
            break
        else:
            continue

    return status


def _toShow(html_str):
    # browser.visit(img_path)
    js = '''document.write("{}")'''.format(html_str)
    browser.reload()
    browser.evaluate_script(js)
    msg = None
    code = None

    for i in range(5):
        # img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        img = browser.find_by_tag('img')
        if img:
            code = 200
            msg = 'ok'
            break
        else:
            code = 500
            msg = 'null'
            time.sleep(0.5)
            continue

    status = (msg,code)

    return status


def zoom(img,rate=2,box=(170,0,580,360)):
    # from PIL import Image
    img = img.crop(box)
    # width = img.size[0]
    # height = img.size[1]
    # img = img.resize((width * int(rate), height * int(rate)), Image.ANTIALIAS)
    # img.show()
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)

    return str(base64_str,encoding='utf-8')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5006)