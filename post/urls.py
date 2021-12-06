from django.urls import path, include
from post.views import BV_PostView, BV_CommentView

urlpatterns = [
    path('<int:pk>/', BV_PostView.as_view()),
    path('<int:pk>/comments', BV_CommentView.as_view())
]
