from njupass import NjuUiaAuth
from dotenv import load_dotenv
import os
import json
import time
import logging
import datetime
from pytz import timezone
from njupass.ocr import detect

URL_JKDK_LIST = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
URL_JKDK_APPLY = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'

auth = NjuUiaAuth()

def get_zjhs_time(method='YESTERDAY'):
    today = datetime.datetime.now(timezone('Asia/Shanghai'))
    yesterday = today + datetime.timedelta(-1)
    if method == 'YESTERDAY':
        return yesterday.strftime("%Y-%m-%d %-H")


if __name__ == "__main__":
    load_dotenv(verbose=True)
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    log = logging.getLogger()

    username = os.getenv('NJU_USERNAME')
    password = os.getenv('NJU_PASSWORD')
    curr_location = os.getenv('CURR_LOCATION')
    method = os.getenv('COVID_TEST_METHOD')

    if method == '':
        method = 'YESTERDAY'

    if username == '' or password == '' or curr_location == '':
        log.error('账户、密码或地理位置信息为空！请检查是否正确地设置了 SECRET 项（GitHub Action）。')
        os._exit(1)

    log.info('尝试登录...')

    if auth.needCaptcha(username):
        log.info("统一认证平台需要输入验证码才能继续，尝试识别验证码...")

    ok = auth.tryLogin(username, password)
    if not ok:
        log.error("登录失败。可能是用户名或密码错误，或是验证码无法识别。")
        os._exit(1)

    log.info('登录成功！')

    for count in range(10):
        log.info('尝试获取打卡列表信息...')
        r = auth.session.get(URL_JKDK_LIST)
        if r.status_code != 200:
            log.error('获取失败，一分钟后再次尝试...')
            time.sleep(60)
            continue

        dk_info = json.loads(r.text)['data'][0]
        if dk_info['TBZT'] == "0":
            wid = dk_info['WID']
            data = "?WID={}&IS_TWZC=1&CURR_LOCATION={}&ZJHSJCSJ={}&JRSKMYS=1&IS_HAS_JKQK=1&JZRJRSKMYS=1&SFZJLN=0".format(
                wid, curr_location, get_zjhs_time())
            url = URL_JKDK_APPLY + data
            log.info('正在打卡')
            auth.session.get(url)
            time.sleep(1)
        else:
            log.info("今日已打卡！")
            os._exit(0)

    log.error("打卡失败，请尝试手动打卡")
    os._exit(-1)
