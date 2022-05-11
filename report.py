from njupass import NjuUiaAuth
import time
import datetime
from pytz import timezone
from urllib.parse import urlencode

URL_JKDK_LIST = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
URL_JKDK_APPLY = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'
URL_JKDK_INDEX = 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.do'


def get_zjhs_time(method='YESTERDAY'):
    """获取最近核酸时间"""
    today = datetime.datetime.now(timezone('Asia/Shanghai'))
    yesterday = today + datetime.timedelta(-1)
    if method == 'YESTERDAY':
        return yesterday.strftime("%Y-%m-%d %-H")


def apply(curr_location, logger, auth: NjuUiaAuth, covidTestMethod='YESTERDAY', force=False):
    """
    完成一次健康打卡
    :param `covidTestMethod`: 最近核酸时间的方案
    :param `force`: 是否在今日已经打卡的前提下强制打卡
    """

    headers = {
        # required since 2022/4/20
        'referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html',
        "X-Requested-With": "com.wisedu.cpdaily.nju",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 cpdaily/8.2.7 wisedu/8.2.7",
        "Host": "ehallapp.nju.edu.cn",
    }
    for _ in range(10):
        logger.info('尝试获取打卡列表信息...')

        auth.session.get(URL_JKDK_INDEX)
        r = auth.session.get(URL_JKDK_LIST, headers=headers)
        if r.status_code != 200:
            logger.error('获取失败，一分钟后再次尝试...')
            time.sleep(60)
            continue

        dk_info = r.json()['data'][0]

        has_applied = dk_info['TBZT'] == "1"
        wid = dk_info['WID']
        param = {
            'WID': wid,
            'IS_TWZC': 1,  # 是否体温正常
            'CURR_LOCATION': curr_location,  # 位置
            'ZJHSJCSJ': get_zjhs_time(covidTestMethod),  # 最近核酸检测时间
            'JRSKMYS': 1,  # 今日苏康码颜色
            'IS_HAS_JKQK': 1,  # 健康情况
            'JZRJRSKMYS': 1,  # 居住人今日苏康码颜色
            'SFZJLN': 0,  # 是否最近离宁
        }

        url = URL_JKDK_APPLY + '?' + urlencode(param)

        if not has_applied or force:
            logger.info('正在打卡')
            auth.session.get(url, headers=headers)

            force = False
            time.sleep(1)

        else:
            logger.info('今日已打卡！')
            return True

    logger.error("打卡失败，请尝试手动打卡")
    return False
