from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, InviteMemberSerializer
from .tasks import send_test_email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .permissions import IsOrgAdmin

User = get_user_model()
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
                'role': user.role,
                'is_active': user.is_active,
                'profile_image': user.profile_image,
                'phone_number': user.phone_number,
                'organization': {
                    'id': user.organization.id,
                    'name': user.organization.name,
                    'email': user.organization.email
                }
            }
            
            return Response({
                "message": "User registered successfully. Check Email to verify", 
                "users": user_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestEmailView(APIView):
    def get(self, request):
        send_test_email.delay()
        return Response({"message": "Test email task has been triggered!"})


class VerifyEmailView(APIView):
    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        if not uid or not token:
            return Response({"error":"Missing uid or token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_active:
            return Response({"message": "Email already verified"}, status=status.HTTP_200_OK)
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({"error": "Account is inactive. Please verify your email."}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access':str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id':user.id,
                'email':user.email,
                'username':user.username,
                'role': user.role,
                'organization': {
                    'id': user.organization.id,
                    'name': user.organization.name,
                    'email': user.organization.email
                }
            }
        })
        
        

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InviteMemberView(APIView):
    permission_classes = [IsAuthenticated, IsOrgAdmin]
    
    def post(self, request):
        serializer = InviteMemberSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "Member invited successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    