# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

'''
设计表userprofile,
可在navicat for mysql
点击查看试试
'''

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default=u"")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("male", u"男"), ("female", "女")), default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username




        # class Meta:
        #     verbose_name = u"课程机构"
        #     verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(max_length=30,
                                 choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email", "修改邮箱")),
                                 verbose_name=u"验证码类型")
    send_time = models.DateField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}[{1}]'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(max_length=100, upload_to="banner/%y%m", verbose_name=u"轮播图")
    url = models.URLField(max_length=100, verbose_name=u"访问地址")
    index = models.IntegerField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        def __init__(self):
            pass

        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
