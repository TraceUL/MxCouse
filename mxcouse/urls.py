#!usr/bin/env python
#-*- coding:utf-8 -*-

"""mxcouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
#django处理静态文件内容
from django.views.static import serve



from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,ActiveUserView



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url('^login/$',LoginView.as_view(),name='login'),
    url('^register/$',RegisterView.as_view(),name='register'),
    url('^captcha/',include('captcha.urls')),
    url('^active/(?P<acthve_code>.*)/$',ActiveUserView.as_view(),name='user_active'),


    #课程机构URL配置
    url(r'^org/',include('organization.urls', namespace="org")),
    url(r'course/',include('courses.urls',namespace="course"))
]
