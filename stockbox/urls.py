"""stockbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django import urls
from django.contrib import admin
from django.db import router
from django.urls import path, include
#from core.models import BV_Post
from rest_framework.urlpatterns import format_suffix_patterns
from core import views
from rest_framework.routers import BaseRouter, DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from core.views import RegisterView 

router = DefaultRouter()
router.register(r'snapshots', views.SnapShotViewSet)
router.register(r'UserProfile', views.UserProfileViewSet)
#router.register(r'Post', views.BV_Post, basename='post')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/' , TokenObtainPairView.as_view()),
    path('api/token/refresh' , TokenRefreshView.as_view()),
    path('api/token/verify' , TokenVerifyView.as_view()),
    path('register/', RegisterView.as_view()),
    #path('api/post/', views.BV_Post)
    path('post/<int:pk>/', views.BV_PostView.as_view()),
]



urlpatterns += static( settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
