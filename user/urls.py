from django.urls import path, include
from user import views

urlpatterns = [
    path('<str:username>/', views.BV_UserView.as_view())
]
