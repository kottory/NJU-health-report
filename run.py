from njupass import NjuUiaAuth
from dotenv import load_dotenv
import os
import json
import time

URL_JKDK_LIST = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
URL_JKDK_APPLY = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'

auth = NjuUiaAuth()

if __name__ == "__main__":
    load_dotenv(verbose=True)
    username = os.getenv('NJU_USERNAME')
    password = os.getenv('NJU_PASSWORD')
    curr_location = os.getenv('CURR_LOCATION')

    if auth.needCaptcha(username):
        print("Captcha is not yet supported, please log in manually.")
        os._exit(1)

    ok = auth.login(username, password)
    if not ok:
        print("Login Failed.")
        os._exit(1)

    print('Login Success')

    for count in range(10):
        r = auth.session.get(URL_JKDK_LIST)
        if r.status_code != 200:
            break

        dk_info = json.loads(r.text)['data'][0]
        if dk_info['TBZT'] == "0":
            wid = dk_info['WID']
            data = "?WID={}&IS_TWZC=1&CURR_LOCATION={}&JRSKMYS=1&IS_HAS_JKQK=1&JZRJRSKMYS=1".format(wid, curr_location)
            url = URL_JKDK_APPLY + data
            auth.session.get(url)
            time.sleep(1)
        else:
            print("Apply Success!")
            os._exit(0)

    print("Apply Failed!")
    os._exit(-1)