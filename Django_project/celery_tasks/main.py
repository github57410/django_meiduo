# -*- coding: utf-8 -*-
"""
   File Name：     main
   Description :
   date：          2019/5/23
   Change Activity:
                   2019/5/23:
"""
__author__ = 'gao_帅帅'

from celery import Celery

# 创建celery应用
celery_app = Celery('meiduo_project')

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

