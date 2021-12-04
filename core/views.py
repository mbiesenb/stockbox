from django.db.models.query import QuerySet
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
#from . models import Snapshot, Tag, UserProfile
#from . serializers import SnapshotSerializer, UserProfileSerializer, RegisterSerializer,  BV_PostSerializer
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import json



# Create your views here.
# http://www.tomchristie.com/rest-framework-2-docs/api-guide/routers



