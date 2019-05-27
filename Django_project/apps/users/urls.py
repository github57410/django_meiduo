# -*- coding: utf-8 -*-
"""
   File Name：     urls
   Description :
   date：          2019/5/23
   Change Activity:
                   2019/5/23:
"""
from django.conf.urls import url

__author__ = 'gao_帅帅'

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 登录获取JWT token
    url(r'authorizations/$', obtain_jwt_token),
]

