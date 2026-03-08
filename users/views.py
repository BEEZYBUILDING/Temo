from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import RefreshToken
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(): #to check if the data(request) recieved is valid
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                #returning status code 201 for successfull creation
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                #returning 400 for error
            )
            
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)
                refresh = str(refresh)
                return Response({
                    'access': access,
                    'refresh': refresh
                },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    'Invalid credentials', status=status.HTTP_400_BAD_REQUEST
                )
                