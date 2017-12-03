#/usr/bin/python
# coding:utf-8

import xadmin
from .models import Course,Lesson,Video,CourseResouce


class CourseAdmin(object):
    list_display=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','teacher_tell']
    search_display=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','teacher_tell']
    list_filter=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']


class LessonAdmin(object):
    list_display=['course','learn_times','name','add_time']
    search_display=['course','learn_times','name']
    list_filter=['course','learn_times','name','add_time']


class VideoAdmin(object):
    list_display =['lesson','name','url','add_time']
    search_display=['lesson','name','url']
    list_filter=['lesson','name','url','add_time']


class CourseResouceAdmin(object):
    list_display =['course','name','download','add_time']
    search_display=['course','name','download']
    list_filter=['course','name','download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResouce,CourseResouceAdmin)


