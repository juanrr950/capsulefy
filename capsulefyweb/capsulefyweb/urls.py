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
from main import views

urlpatterns = [
    path(r'', views.index),
    path('displaycapsule/<int:id>/', views.displayCapsules, name='displaycapsule'),
    path('list/', views.list,  name='list'),
    path('newmodularcapsule/', login_required(views.createModularCapsule), name='createmodularcapsule'),
    path('editmodularcapsule/<int:pk>/', login_required(views.editModularCapsule), name='editmodularcapsule'),
    path('admin/', admin.site.urls),
    
    path('login/', views.login.as_view(),name='login'),  
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]
