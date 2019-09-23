import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User
from ..settings import UPLOAD_DIR
from django.http import JsonResponse, HttpResponse
