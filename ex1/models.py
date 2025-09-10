# models are basically db relations as python ORM classes
# can consider sql but on steroids
# Various type of fields - CharField, IntegerField, FloatField, DateTimeField, ForeignKey, ManyToManyField, OneToOneField
# Various type of field options - max_length, unique, blank, null, default, choices
# ForeignKey - on_delete options - CASCADE, SET_NULL, PROTECT, SET_DEFAULT
# ManyToManyField - related_name option to access reverse relation
# OneToOneField - similar to ForeignKey with unique constraint

# There are also some default django models for auth, permissions, groups etc
# Some are BaseUserManager, AbstractBaseUser, PermissionsMixin mainly for custom user
# For default user model, can use from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )
    
    def set_password(self, raw_password):
        return super().set_password(raw_password)

    def __str__(self):
        return self.email



class CountryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, unique=True)
    curr_symbol = models.CharField(max_length=1)
    phone_code = models.CharField(max_length=10, unique=True)
    my_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name='countries', null=True, on_delete=models.SET_NULL)
    
    """
    Observation:
    
    For my_user, i can have null=True, with on_delete=models.SET_NULL
    or if i dont have null field, i need to have default field with on_delete=models.CASCADE
    if i have null=True with on_delete=models.CASCADE, DJango will ask to put a default value when creating a migration
    on_delete field is mandatory since my_user is a ForeignKey
    
    null=False, on_delete=models.CASCADE, default=None -> All good
    null=True, on_delete=models.SET_NULL -> All good
    null=False, on_delete=models.CASCADE -> Error while creating migration (need default value)
    null=False, on_delete=models.SET_NULL -> System check error (abruptly stop process)
    """

    def __str__(self):
        return self.name

class StateModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    gst_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    state_code = models.CharField(max_length=10, unique=True)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, related_name='states')
    
    class Meta: 
        unique_together = ['name', 'country']

    def __str__(self):
        return self.name

class CityModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10, unique=True)
    phone_code = models.CharField(max_length=10, unique=True)
    population = models.IntegerField()
    avg_age = models.FloatField()
    num_of_adults_males = models.PositiveBigIntegerField()
    num_of_adults_females = models.PositiveBigIntegerField()
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name='cities')
    
    class Meta:
        unique_together = ['name', 'state']
        
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.population <= (self.num_of_adults_males + self.num_of_adults_females):
            raise ValidationError('Population must be greater than the sum of adult males and females.')
        
    def __str__(self):
        return self.name
