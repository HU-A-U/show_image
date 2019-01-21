# -*- coding:utf-8 -*-
import time
from flask import request
from splinter import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from flask import Flask
from config import Config
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
    if not data:
        if not request.form:
            res['msg'] = '没有数据'
        else:
            img_path = request.form.get('img_path', '')
    else:
        img_path = request.json.get('img_path', '')

    # from tasks import _toShow
    # status = _toShow.delay(img_path)
    for i in range(3):
        status = _toShow(img_path)
        if status[0] == 200:
            break
        else:
            continue

    return status


def _toShow(img_path):
    browser.visit(img_path)
    msg = None
    code = None
    for i in range(5):
        img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005)
