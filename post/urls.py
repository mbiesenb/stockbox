from django.urls import path, include
from user import views

urlpatterns = [
    path('<int:pk>/', views.BV_UserView.as_view())
]
