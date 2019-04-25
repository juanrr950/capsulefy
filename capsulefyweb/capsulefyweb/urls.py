"""capsulefyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from main import views, views_user, views_admin
from main.admin import admin_site

urlpatterns = [
    path('', views.index),
    path('admin/', admin_site.urls),
    path('displaycapsule/<int:id>/', views.displayCapsules, name='displaycapsule'),
    path('list/<str:type>/', views.list,  name='list'),
    path('newmodularcapsule/', login_required(views.createModularCapsule), name='createmodularcapsule'),
    path('newmodule/<int:pk>/', login_required(views.createModule), name='createmodule'),
    path('editmodularcapsule/<int:pk>/', login_required(views.editModularCapsule), name='editmodularcapsule'),
    path('editmodule/<int:pk>/', login_required(views.editModule), name='editmodule'),
    path('deletemodule/<int:pk>/', login_required(views.deleteModule), name='deletemodule'),
    path('newfreecapsule/', views.createFreeCapsule, name='createfreecapsule'),
    path('editfreecapsule/<int:pk>/', views.editFreeCapsule, name='editfreecapsule'),
    path('deletecapsule/<int:pk>/', views.deleteCapsule, name='deletecapsule'),
    path('deletefile/<int:pk>/', views.deleteFile, name='deletefile'),
    path('deletefreefile/<int:pk>/', views.deleteFreeFile, name='deletefreefile'),
    path('login/', views.login.as_view(),name='login'),
    path('accounts/login/', views.login.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('select_capsule/', views.select_capsule),
    path('refresh/<int:id>/', views.refresh_deadman, name='refreshdeadman'),
    path('ajaxlist/<str:type>', views.ajaxlist),
    path('register/', views_user.register),
    path('payment/execute/', views.paymentExecute),
    path('user/myaccount/', views.my_account, name='myaccount'),
    path('user/logintwitter/', views.login_twitter, name='logintwitter'),
    path('user/successtwitter/', views.success_twitter, name='successtwitter'),
    path('adm/list/', views_admin.list),
    path('adm/dashboard/', views_admin.dashboard),
    path('ajaxban/', views_admin.ajax_ban),
    path('update/', views.update,name='update'),
    path('deleteUser/', views_user.deleteUser),
    path('user/notifemail/', views.update_notifemail, name='notifemail'),
    path('terms', views.terms,name='terms'),
]
