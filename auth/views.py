from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User


from auth.serializers import RegisterSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    #permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
#mixins.ListModelMixin,  viewsets.GenericViewSet