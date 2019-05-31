from django.contrib.auth.models import AbstractUser
from django.db import models
# from Django_project import settings
# 导入django系统默认的配置文件
from django.conf import settings
from . import constants
# 在User模型类中实现使用TimedJSONWebSignatureSerializer可以生成带有有效期的token
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
# 导入django系统默认的配置文件


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    # id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_send_sms_token(self):
        """
        生成发送短信验证码的token
        """
        # itsdangerous模型实例,第一个参数为配置密钥,第二个为过期时间
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.SEND_SMS_TOKEN_EXPIRES)
        data = {
            'mobile': self.mobile
        }
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_send_sms_code_token(token):
        """
        检验发送短信验证码的token
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.SEND_SMS_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            return data.get('mobile')

    def generate_set_password_token(self):
        """
        生成修改密码的token
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.SET_PASSWORD_TOKEN_EXPIRES)
        # 模型类
        data = {'user_id': self.id }
        token = serializer.dumps(data)
        return token.decode()



    @staticmethod
    def check_set_password_token(token, user_id):
        """
        检验设置密码的token
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.SET_PASSWORD_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return False
        else:
            if user_id != str(data.get('user_id')):
                return False
            else:
                return True
