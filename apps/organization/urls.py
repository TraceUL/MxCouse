#!usr/bin/env python  
#-*- coding:utf-8 -*-

from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgCourseView,OrgDescView,OrgHomeView,OrgTeacherView,TeacherListView,AddFavView
from .views import TeacherDetailView




urlpatterns = [
    url(r'^list/$',OrgView.as_view(),name="org_list"),
    url(r'^add_ask/$',AddUserAskView.as_view(),name="add_ask"),
    url(r'^home/(?P<org_id>\d+)$',OrgHomeView.as_view(),name="org_home"),#http://127.0.0.1:8000/org/home/1
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(),name="org_teacher"),


    #讲师列表
    url(r'^teacher/list$',TeacherListView.as_view(), name="add_fav"),

    #机构列表
    url(r'^add_fav/$',AddFavView.as_view(),name="add_fav"),


    #讲师列表
    url(r'^teacher/list/$',TeacherListView.as_view(),name="teacherlist"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$',TeacherDetailView.as_view(),name="teacherdetail")




]