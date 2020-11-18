from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Profile(models.Model): 

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = PhoneNumberField(blank=True)
    
    
