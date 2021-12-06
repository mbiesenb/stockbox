from django.urls import path, include

from core.views import BV_ChatView, BV_ChatMessageView

urlpatterns = [
    path('chats/', BV_ChatView.as_view()),
    path('chats/<int:pk>/messages', BV_ChatMessageView.as_view())
]
