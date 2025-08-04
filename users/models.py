from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ORG_ADMIN', 'Organization Admin'),
        ('ORG_MEMBER', 'Organization Member'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ORG_ADMIN')
    is_active = models.BooleanField(default=True)
    profile_image = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='users',
        null=False,
        blank=False
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
