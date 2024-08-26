from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from users.serializers import UserSerializer
from users.models import User


class RegisterView(APIView):
    def post(self, request):
        """_summary_
        회원가입에 사용하는 API

        request:
            required:
                username: str
                password: str
            optional:
                first_name: str
                last_name: str
                email: str
        """
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data="Registered", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        """_summary_
        로그인에 사용하는 API

        request:
            required:
                username: str
                password: str
        """
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            })
        else:
            return Response(
                data="Invalid credentials", 
                status=status.HTTP_400_BAD_REQUEST
            )
