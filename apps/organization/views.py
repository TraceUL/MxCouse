#!usr/bin/env python
#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render


from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from .models import CourseOrg,CityDict,Teacher
from operation.models import UserFavorite
from courses.models import Course
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from forms import UserAskForm


class TeacherDetailView(View):
    def get(self,request,teacher_id):
     teacher= Teacher.objects.get(id= int(teacher_id))
     teacher.click_nums +=1
     teacher.save()
     all_courses = Course.objects.filter(teacher = teacher)


     has_teacher_faved = False
     if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
         has_teacher_faved = True
     if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org_id):
         has_org_faved = True

     #讲师排行
     sorted_teacher = Teacher.objects.order_by("-click_nums")[:3]
     return render(request,"teacher-detail.html",{
         "teacher":teacher,
         "all_courses":all_courses,
         "sorted_teacher":sorted_teacher,
         "has_teacher_faved":has_teacher_faved,
         "has_org_faved": has_org_faved,

     })




class AddFavView(View):
    '''
    用户收藏
    '''
    def post(self,request):
        fav_id = request.POST.get("fav_id",0)
        fav_type = request.POST.get("fav_type",0)

        if not request.user.is_authenticated():
            """此处为一个匿名类,django内置的一种方法,此user与征程的user有像是的用法
            所以此处调用user.is_authenticated()方法，后面带括号,
            """
            return HttpResponse('{"status"："fail","mas":"用户没登陆"}',content_type="application/json")
        exit_recods= UserFavorite.objects.filter(user = request.user,fav_id = int(fav_id),fav_type= int(fav_type))
        if exit_recods:
            """记录已经存在，则表示要取消收藏"""
            exit_recods.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums <= 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <= 0:
                    course_org.fav_nums = 0
                course_org.save()

            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status": "fail", "msg":"收藏出错"}', content_type="application/json")

class TeacherListView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all()

        current_nav = "teacher"


        #关键词搜索功能
        search_keywords = request.GET.get("keywords","")

        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords)|Q(word_company_icontains=search_keywords)
                #name_icotains django 会把name转换为like语句
                #django 的model中，出现了i，则不区分大小写


            )
        #讲师排序
        sort = request.GET.get("sort","")
        if sort:
            if sort=="hot":
                all_teachers = all_teachers.order_by(("-click_nums"))

        #讲师排行
        sorted_teacher= Teacher.objects.order_by("-click_nums")[:3]

        #对讲师进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1


        p = Paginator(all_teachers,3,request=request)
        teachers = p.page(page)
        return render(request,"teachers-list.html",{
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,
            "sorted":sort,
            "current_nav":current_nav,
        })


class OrgView(View):
    '''课程机构列表

    '''

    def get(self,request):
        all_orgs = CourseOrg.objects.all()   #取值后用filter过滤
        all_citys = CityDict.objects.all()
        hot_orgs=all_orgs.order_by("-click_nums")[:3]

        #取出筛选城市
        city_id=request.GET.get("city","")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

         # 类别筛选
        catogry=request.GET.get("ct","")
        if catogry:
            all_orgs =all_orgs.filter(catgory=catogry)

        #关键词搜索功能
        search_keywords = request.GET.get("keywords","")
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(neme_icontains=search_keywords)|Q(desc__icontains=search_keywords)
            # name__icontains django会把name转换为like语句
            # django的model中，出现了i，则不区分大小写
            )

        #排序
        sort = request.GET.get("sort","")
        if sort:
            if sort =="students":
                all_orgs = all_orgs.order_by("-students")
            elif sort =="courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()



        #对课程机构进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,4,request=request)

        orgs = p.page(page)

        return render(request,"org-list.html",
                      {"all_orgs":orgs,
                       "all_citys":all_citys,
                       "org_nums":org_nums,
                       "city_id":city_id,
                       "catgory":catogry,
                       "hot_orgs":hot_orgs,
                       "sort":sort

                       })

class AddUserAskView(View):
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)
            return HttpResponse('{"status":"success}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type="application/json")



class OrgCourseView(View):
    """机构课程列表
    """
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses= course_org.course_set.all()
        #有外键的地方都可以这么取值
        return render(request, 'org-detail-course.html',{
            "all_courses": all_courses,
            "course_page": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })




class OrgHomeView(View):
        '''
        机构首页
        '''
        def get(self,request,org_id):
            current_page="home"
            course_org = CourseOrg.objects.get(id=int(org_id))
            has_fav=False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                    has_fav=True
            all_courses = course_org.course_set.all()[:3]
            #有外键地方都可以这么取值
            all_teachers = course_org.teacher_set.all()[:1]
            return render(request,'org-detail-homepage.html',
                          {
                              "course_org":course_org,
                              "current_page":current_page,
                              "has_fav":has_fav,
                          }
                          )

class OrgDescView(View):

    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,

        })
class OrgTeacherView(View):
    '''机构讲师'''
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id= int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav= False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id= course_org.id,fav_type=2):
                #有外键地方都可以这么取值
                has_fav=True
        return render(request,'org-detail-teachers.html',{
            "course_org":course_org,
            "all_teachers":all_teachers,
            "current_page":current_page,
            "has_fav":has_fav,
        })