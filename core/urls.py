
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name="home"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('logout/',views.logout,name="logout"),
    path('createGroup/',views.createGroup,name="createGroup"),
    path('group/<name>/',views.group,name="group"),
    path('addmember/<int:groupId>/',views.addmember,name="addmember"),
    path('api/group/<int:groupId>/findOne/',views.findOne,name="findOne"),
    path('api/group/<int:groupId>/findMultiple/',views.findMultiple,name="findMultiple"),
    path('api/all/findOne/',views.findAllOne,name="findAllOne"),
    path('api/all/findMultiple/',views.findAllMultiple,name="findAllMultiple")
]
