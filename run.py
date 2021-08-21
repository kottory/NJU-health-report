from njupass import NjuUiaAuth
from dotenv import load_dotenv
import os
import json
import time
import logging

URL_JKDK_LIST = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
URL_JKDK_APPLY = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'

auth = NjuUiaAuth()

if __name__ == "__main__":
    load_dotenv(verbose=True)
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    log = logging.getLogger()

    username = os.getenv('NJU_USERNAME')
    password = os.getenv('NJU_PASSWORD')
    curr_location = os.getenv('CURR_LOCATION')

    log.info('Trying to login...')

    if auth.needCaptcha(username):
        log.error("Captcha is not yet supported, please log in manually.")
        os._exit(1)

    ok = auth.login(username, password)
    if not ok:
        log.error("Login Failed.")
        os._exit(1)

    log.info('Login Success')

    for count in range(10):
        log.info('Trying to get jkdk list...')
        r = auth.session.get(URL_JKDK_LIST)
        if r.status_code != 200:
            log.info('Getting jkdk list failed!')
            time.sleep(60)
            continue

        dk_info = json.loads(r.text)['data'][0]
        if dk_info['TBZT'] == "0":
            wid = dk_info['WID']
            data = "?WID={}&IS_TWZC=1&CURR_LOCATION={}&JRSKMYS=1&IS_HAS_JKQK=1&JZRJRSKMYS=1".format(
                wid, curr_location)
            url = URL_JKDK_APPLY + data
            log.info('Applying...')
            auth.session.get(url)
            time.sleep(1)
        else:
            log.info("Apply Success!")
            log.info("Your location is {}".format(dk_info["CURR_LOCATION"]))
            os._exit(0)

    log.error("Apply Failed!")
    os._exit(-1)
