from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from decouple import config

@shared_task
def send_verification_email(email, activation_link):
    subject = 'Verify Your Email - Budget App'
    message = f"Click the link to verify your account: {activation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    
    
def test_celery():
    print("🎉 Hello from Celery!")
    return "It works!"

@shared_task
def send_test_email():
    send_mail(
        subject='Test Email from Django + Celery',
        message='Hello! This is a test email to confirm your Celery and email setup.',
        from_email=config('EMAIL_HOST_USER'),  # Replace with your configured sender
        recipient_list=['joelayomide35@gmail.com'],  # Replace with your actual email
        fail_silently=False,
    )
    
@shared_task
def send_invitation_email(email, password, org_name):
    subject = "You've hav been invited to join an organization"
    message = f"""
Hi there!

You've been added to the organization "{org_name}".

Here are your login details:
Email: {email}
Password: {password}

Please log in and change your password.

Best,
Budget App Team
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])