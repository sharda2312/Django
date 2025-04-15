from django.core.mail import send_mail
from django.conf import settings

def send_otp(email, otp):
    subject = "Your OTP Code"
    message = f"Hello,\n\nYour OTP is: {otp}\nIt will expire in 10 minutes.\n\nThanks!"
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, email_from, recipient_list)