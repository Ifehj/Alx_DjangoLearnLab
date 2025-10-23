from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import login, get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
User = get_user_model()
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

class FollowUserView(generics.GenericAPIView):
      permission_classes = [IsAuthenticated]

      def post(self, request, user_id, *args, **kwargs):
            target = get_object_or_404(User, pk=user_id)
            # prevent following yourself
            if target == request.user:
                  return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            if request.user.following.filter(pk=target.pk).exists():
                  return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.following.add(target)
            request.user.save()
            return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)

    
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        target = get_object_or_404(User, pk=user_id)

        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.following.filter(pk=target.pk).exists():
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)
        request.user.save()
        return Response({"detail": f"You unfollowed {target.username}."}, status=status.HTTP_200_OK)