# -*- coding: utf-8 -*-
"""
   File Name：     tasks
   Description :
   date：          2019/5/23
   Change Activity:
                   2019/5/23:
"""


__author__ = 'gao_帅帅'

from Django_project.celery_tasks.main import celery_app
from Django_project.libs.yuntongxun.sms import CCP
import logging
from . import constants


logger = logging.getLogger("django")

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_code: 验证码时效
    :return: None
    """

    time = str(constants.SMS_CODE_EXPIRES)
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_CODE_TEMP_ID)
        print(result)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)