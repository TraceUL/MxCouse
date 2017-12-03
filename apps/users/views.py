#coding:utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q   #相当于or
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  #对明文进行加密
from django.http import HttpResponse,HttpResponseRedirect

from .models import UserProfile,EmailVerifyRecord   #传进file便于查询
from .forms import LoginForm,RegisterForm
from operation.models import UserMessage
from utils1.email_send import send_register_email




class ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for recode in all_records:
                email=recode.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")



#注册
class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,"register.html",{'register_form':register_form})
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name=request.POST.get("email","")
            pass_word=request.POST.get("password","")
            if UserProfile.objects.filter(email=user_name):
                return render(request,"register.html",{"register_form":register_form,"msg":"用户已存在 "})
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.is_active=False
            #对明文密码进行加密
            user_profile.password=make_password(pass_word)
            user_profile.save()



            # user_message=UserMessage()
            # user_message.user=user_profile.id
            # user_message.message="欢迎注册"
            # user_message.save()

            # send_register_email(user_name,"register")
            print u"success"
            return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_form})


#用用户名or邮箱登陆
class CutomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
        login_form=LoginForm(request.POST)#用于验证用户名和密码的参数
        if login_form.is_valid():
            user_name= request.POST.get("username","")
            pass_word=request.POST.get("password","")
            user=authenticate(username=user_name,password=pass_word)
            if user is not None:    #?????
                if user.is_active:
                    login(request,user)
                    return render(request,'index.html')
                else:
                    return render(request,"login.html",{"msg":"用户未激活"})
            else:
                return render(request,"login.html",{"msg":"用户名密码错误"})
        else:
            return render(request,"login.html",{"login_form":login_form})

#函数登陆，因为已经用loginview类登陆，所以废弃,类登陆逻辑更好
# Create your views here.
# def user_login(request):
#     if request.method=="POST":
#         user_name=request.POST.get("username","")
#         pass_word=request.POST.get("password","")
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误！"})
#     elif request.method=="GET":
#         return render(request,'login.html',{})