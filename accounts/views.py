from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import Team
from accounts.serializers import UserRegisterSerializer, EmailLoginSerializer, TeamSerializer


class TeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.filter(is_assembler=False)


class LoginView(APIView):
    serializer_class = EmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Kullanıcıyı email ile doğrula
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Kullanıcı doğrulandı, token'ı al
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
