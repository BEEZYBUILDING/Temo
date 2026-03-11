from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address
from .permissions import IsAdmin
from .serializers import RegisterSerializer, LoginSerializer, AddressSerializer
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
                #returning status code 201 for successfull creation
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
        
        serializer = AddressSerializer(address, data=request.data)
        