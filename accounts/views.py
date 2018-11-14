from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class UserCreate(APIView):

    def post(self, request):
        print('I am in post view')
        serializer = UserSerializer(data=request.data)
        print('HIIIIIIII', serializer)
        print(serializer.errors)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#login api
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)