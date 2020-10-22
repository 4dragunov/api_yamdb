# import secrets
# import string
#
# from django.contrib.auth import authenticate
# from django.core.mail import send_mail
# from django.shortcuts import render, get_object_or_404
# from rest_framework import status, viewsets
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated
#
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from .serializers import UserSerializer, UserEmailSerializer, \
#     UserLoginSerializer
#
# from .models import User
#
