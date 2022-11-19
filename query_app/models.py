from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django.core.validators import RegexValidator

domain_validator = RegexValidator(
    regex='@(pg.com)$',
    message='Only p&g id is allowed',
    code='invalid_domain',
)

class Regions(models.Model):  
    
    class Meta:
        verbose_name_plural = 'Regions'    
             
    Region = models.CharField(max_length=10, primary_key=True)
    DB_Host = models.CharField(max_length=100)
    DB_Service_Name = models.CharField(max_length=50)
    DB_Port = models.IntegerField()
    
    def __str__(self):
        return self.Region


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, validators=[domain_validator])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_email_verified = models.BooleanField(default=False)
    regions = models.ManyToManyField('Regions', blank=True, related_name="regions")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


    
    
class Reports(models.Model):
    
    class Meta:
        verbose_name_plural = 'Reports' 
        
    Report_Name = models.CharField(max_length=200)
    Sql_Query = models.TextField()
    Region = models.ForeignKey(Regions, on_delete=models.CASCADE, blank=False, default='Unspecified')
    # Data_Fetched = models.TextField(null=True, blank = True)
    Last_Run = models.DateTimeField(blank=True, null=True)
    Task_Status = models.CharField(max_length=15, default = "Not Running")
    Task_Id = models.CharField(max_length = 70, blank = False, null = True)
    
    
    
    def __str__(self):
        return self.Report_Name
    
class Reports_Data(models.Model):
    
    class Meta:
        verbose_name_plural = 'Reports Data' 
        
    Report_Name = models.CharField(max_length=200, null=True, blank = True)
    Data_Fetched = models.TextField(null=True, blank = True)
    
    
    
    def __str__(self):
        return self.Report_Name
    