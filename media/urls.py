from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from media.views import BV_MediaView, BV_ProfileImageView


## IMPOORTANT: REMOVE CSRF EXEMPT
urlpatterns = [
   path('', BV_MediaView.as_view()),
   path('profileimage/', BV_ProfileImageView.as_view() )
]