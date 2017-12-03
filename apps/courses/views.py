#!usr/bin/env python
#-*- coding:utf-8 -*-


from django.shortcuts import render


from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments,UserCourse
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from utils1.mixin_utils import LoginRequireMixin


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]


        #关键词搜索功能
        search_keywords= request.GET.get("keywords","")
        if search_keywords:
            all_courses= all_courses.filter(Q(name__icontains=search_keywords)|Q(desc_icontains= search_keywords|Q(detail_icontains=search_keywords)))

        sort = request.GET.get("sort","")
        if sort:
            if sort=="students":
                all_courses = all_courses.order_by("-students")
            elif sort =="hot":
                all_courses = all_courses.order_by("-click_nums")

        #对课程进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses,3,request=request)

        courses = p.page(page)
        return render(request,"course-list.html",{
            "all_courses":all_courses,
            "hot_courses":hot_courses,
            "sort":sort,
        })



class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id = int(course_id))

        #增加课程点击数
        course.click_nums += 1
        course.save()
        return render(request,"course-detail.html",{
            "course":course,
        })


class CourseInfoView(LoginRequireMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id = int(course_id))
        course.students +=1
        course.save()


        all_resourses = CourseResource.objects.filter(course = course)
        user_courses = UserCourse.objects.filter(course = course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_course =UserCourse.objects.filter(user_id__in= user_ids)

        """
        user_id__in
        django的用法，获取一个列表内容
        
        """
        course_ids = [user_course.id for user_course in user_courses]
        relate_courses=Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

        return render(request,"course-video.html",{
            "course":course,
            "course_resources":all_resourses,
            "relate+courses":relate_courses,

        })
class CommentsView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html",{
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments,


        })


class AddCommentsView(View):
    """
    添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            """
            此处user为一个匿名类，django内置的一种方法，此user与正常的user有相似的用法
            所以此处调用user.is_authenticated()方法，后面带括号.
            """
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type="application/json")

        courser_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if courser_id > comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(courser_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg":"添加失败"}', content_type="application/json")



