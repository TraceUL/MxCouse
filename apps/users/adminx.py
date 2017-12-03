# /usr/bin/python
# coding:utf-8

import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    enable_thems=True
    use_bootswath=True

class GlobalSetting(object):
    site_title='后台管理'
    site_footer='在线教育视频'
    menu_style='accordion'



class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display=['title','image','url','index','add_time']
    search_fields=['title','image','url','index']
    list_filter=['title','image','url','index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)#设置全局  例如收起列表
xadmin.site.register(views.CommAdminView,GlobalSetting)


