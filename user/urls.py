from django.urls import path, include
from user import views

urlpatterns = [
    path('', views.BV_UserView.as_view())
]
