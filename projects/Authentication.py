from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class Students(object):
   email = models.EmailField(unique=True, max_length=100)
   password = models.CharField(max_length=128)

class Supervisor(object):
   email = models.EmailField(unique=True, max_length=100)
   password = models.CharField(max_length=128)

class Oydessy(object):
   email = models.EmailField(unique=True, max_length=100)
   password = models.CharField(max_length=128)



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_supervisor(self, email, password):
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_odyssey(self,email, password):
    	user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
