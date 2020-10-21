import secrets
import string

from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserEmailSerializer

from .models import User

def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(secrets.choice(chars) for _ in range(size))

'''Обработка POST запроса на получение Confirmation code'''
class Confirmation_code(APIView):
    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            if User.objects.filter(email=email):
                return Response('Пользователь уже зарегестрирован в системе',
                    status=status.HTTP_410_GONE)
            User.objects.create(username=email, email=email)
            Confirmation_code = id_generator()
            send_mail('Ваш секретный код', Confirmation_code,
                      'admin@yamdb.com', [email],
                      fail_silently=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




