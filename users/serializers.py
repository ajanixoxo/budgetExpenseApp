from rest_framework import serializers
from .models import User
from organizations.models import Organization
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from users.tasks import send_verification_email  # Celery task
import random
import string
from .tasks import send_invitation_email


class RegisterSerializer(serializers.Serializer):
    # Organization fields
    org_name = serializers.CharField()
    org_email = serializers.EmailField()

    # User fields
    user_email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        # 1. Create organization
        org = Organization.objects.create(
            name=validated_data['org_name'],
            email=validated_data['org_email']
        )

        # 2. Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['user_email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role='ORG_ADMIN',
            organization=org,
            phone_number=validated_data.get('phone_number', None),
            profile_image=validated_data.get('profile_image', None),
            is_active=False  # User must verify email
        )

        # 3. Generate email verification token
        token = default_token_generator.make_token(user)

        # 4. Construct frontend verification link
        activation_link = f"{settings.FRONTEND_URL}/verify-email/?uid={user.pk}&token={token}"

        # 5. Send email in background using Celery
        send_verification_email.delay(user.email, activation_link)

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'profile_image',
            'phone_number', 'organization'
        ]
        read_only_fields = ['id', 'email', 'role', 'organization']
        

class InviteMemberSerializer(serializers.Serializer):
   first_name = serializers.CharField(required=True)
   last_name= serializers.CharField(required=True)
   email = serializers.EmailField(required=True)
   phone_number = serializers.CharField(required=False, allow_blank=True)
   
   def create(self, validated_data):
       request = self.context['request']
       org_admin = request.user
       organization = org_admin.organization
       
       
    #    radnom password generation
       password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
       
       user = User.objects.create_user(
           username=validated_data['email'].split('@')[0],  # Use email prefix as username
           email=validated_data['email'],
           password=password,
           first_name=validated_data['first_name'],
           last_name=validated_data['last_name'],
           phone_number=validated_data.get('phone_number', None),
           organization=organization,
           role='ORG_MEMBER',  # Default role for invited members
           is_active=True  
       )
       
       send_invitation_email.delay(
           user.email,
           password,
           organization.name,
       )
       return user