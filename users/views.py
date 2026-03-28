from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address
from cart.services import CartService
from .permissions import IsAdmin
from .serializers import (RegisterSerializer, LoginSerializer, 
                          AddressSerializer, UserProfileSerializer,
                          ChangePasswordSerializer)
from .tokens import CustomRefreshToken

# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(): #to check if the data(request) recieved is valid
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                #returning status code 201 for successfull creation and the data back
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                #returning 400 for error
            )
            
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user:
                session_token = request.headers.get('X-Session-Token')
                if session_token:
                    CartService.merge_carts(user.id, session_token)
            
                refresh = CustomRefreshToken.for_user(user)
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
                
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            #refresh token is used to blacklist the token  
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response("success", status=status.HTTP_200_OK)
        except Exception:  #if token in invalid
            return Response('Cant logout', status=status.HTTP_400_BAD_REQUEST)
    
class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddressUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        try:
            address = Address.objects.get(id=pk, user=request.user)#fetch a specific address
        except Address.DoesNotExist:
            return Response("Invalid address", status=status.HTTP_404_NOT_FOUND) 
        
        serializer = AddressSerializer(address, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            address = Address.objects.get(id=pk, user=request.user)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response("Does not exist", status=status.HTTP_404_NOT_FOUND)
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user) #serializing the the single object(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                return Response('Password changed successfully', status=status.HTTP_200_OK)
            else:
                return Response('wrong password', status=status.HTTP_400_BAD_REQUEST)
        else:
                return Response('bad request', status=status.HTTP_400_BAD_REQUEST)
        