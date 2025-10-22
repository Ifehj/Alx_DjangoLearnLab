from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import login
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
# Create your views here.

class RegisterView(generics.CreateAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = RegisterSerializer
	permission_classes = [AllowAny]
	
	def create(self, request, *args, **kwargs):
        # validate incomint data
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
        # save user
		user = serializer.save()
        # create token for the user
		token, created = Token.objects.get_or_create(user=user)
        # return response with user data and token
		return Response({
			"user": UserSerializer(user).data,
			"token": token.key
		}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })
