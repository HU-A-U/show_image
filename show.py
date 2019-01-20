# -*- coding:utf-8 -*-
import time
from flask import Flask, jsonify
from flask import render_template
from flask import request
from config import Config

app = Flask(__name__)
# 配置
app.config.from_object(Config)

from splinter import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
    status = _toShow(img_path)

    return 'ok',status


def _toShow(img_path):
    browser.visit(img_path)
    msg = None
    code = None
    for i in range(5):
        img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        if img:
            code = 222
            msg = 'ok'
            break
        else:
            code = 111
            msg = 'null'
            time.sleep(0.5)
            continue

    status = {
        'msg':msg,
        'code':code
    }

    return status

if __name__ == '__main__':
    app.run()
