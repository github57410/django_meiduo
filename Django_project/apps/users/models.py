from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from itsdangerous import BadData
from Django_project.settings import dev

from Django_project.apps.users import constants


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_send_sms_token(self):
        """
        生成发送短信验证码的token
        """
        # itsdangerous模型实例,第一个参数为配置密钥,第二个为过期时间
        serializer = TJWSSerializer(dev.SECRET_KEY, expires_in=constants.SEND_SMS_TOKEN_EXPIRES)
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
        serializer = TJWSSerializer(dev.SECRET_KEY, expires_in=constants.SEND_SMS_TOKEN_EXPIRES)
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
        serializer = TJWSSerializer(dev.SECRET_KEY, expires_in=constants.SET_PASSWORD_TOKEN_EXPIRES)
        data = {'user_id': self.id}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_set_password_token(token, user_id):
        """
        检验设置密码的token
        """
        serializer = TJWSSerializer(dev.SECRET_KEY, expires_in=constants.SET_PASSWORD_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return False
        else:
            if user_id != str(data.get('user_id')):
                return False
            else:
                return True
