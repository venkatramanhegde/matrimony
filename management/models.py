from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
import os
# Create your models here.
import rest_framework.authtoken.models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


def get_file_path(instance, associated_profile_path):
    return os.path.join('media/', associated_profile_path)


class User(AbstractBaseUser):
    """this tables consist information about user"""
    first_name = models.CharField(max_length=60, null=False)
    father_name = models.CharField(max_length=60, blank=True)
    phone_no = models.CharField(max_length=25, null=False, unique=True)
    password = models.CharField(max_length=256)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_male = models.BooleanField()
    is_female = models.BooleanField()
    is_approved = models.BooleanField(default=False)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    email = models.EmailField(verbose_name='email address',
                              max_length=100,
                              null=True
                              )
    is_reject = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'phone_no'


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=False)
    hav_id = models.CharField(max_length=25, default="TSS2842")
    first_name = models.CharField(max_length=60, null=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_no = models.CharField(max_length=25, null=False, unique=True)
    password = models.CharField(max_length=256)
    is_male = models.BooleanField(default=False)
    is_female = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, null=True, blank=False)
    email = models.EmailField(verbose_name='email address',
                              max_length=100,
                              null=True
                              )
    is_approved = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    age = models.IntegerField(null=True, blank=True)
    father_name = models.CharField(max_length=60, blank=True, null=True)
    mother_name = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    caste = models.CharField(max_length=50, blank=True, null=True)
    gotra = models.CharField(max_length=50, blank=True, null=True)
    nakshatra = models.CharField(max_length=50, blank=True, null=True)
    rashi = models.CharField(max_length=50, blank=True, null=True)
    material_status = models.CharField(max_length=50, blank=True, null=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    job_position = models.CharField(max_length=100, blank=True, null=True)
    highest_education = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=60, blank=True, null=True)
    company_name = models.CharField(max_length=60, blank=True, null=True)
    # qualificationandoccupation = models.CharField(max_length=100, null=True, blank=True)
    # requirements = models.CharField(max_length=500, null=True, blank=True)

    horoscope = models.FileField(upload_to=get_file_path, blank=True, null=True)
    photos = ArrayField(models.CharField(max_length=500), null=True)
    photo1 = models.FileField(upload_to=get_file_path, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)



class Education(models.Model):
    degree_name = models.CharField(max_length=100)


class Religion(models.Model):
    religion_name = models.CharField(max_length=75)


class Caste(models.Model):
    caste_name = models.CharField(max_length=75)



class Token(rest_framework.authtoken.models.Token):
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    session_time = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
