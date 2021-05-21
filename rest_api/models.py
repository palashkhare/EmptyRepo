from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class UserProfileModelManager(BaseUserManager):
    """Customize user model manager"""

    def create_user(self, name, email, password=None):
        """Override Create user function of default user Manager"""
        if not email or not name:
            raise ValueError("Name and Email are mandatory")

        email = self.normalize_email(email)
        user = self.model(name=name, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, email, password):
        """ Override Superuser function"""
        user = self.create_user(name, email, password)

        user.is_superuser = True
        user.is_family = True
        user.is_staff = True

        return user

class UserProfileModel(AbstractBaseUser, PermissionsMixin):
    """Modify base user model"""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_family = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def get_full_name(self):
        """Return Full name string"""
        return self.name

    def get_email(self):
        """Return Email ID"""
        return self.email

    def __str__(self):
        """define string"""
        return self.name

class UserFeeds(models.Model):
    """Define a custom user feed model"""
    userProfile = models.ForeignKey(
        UserProfileModel,
        on_delete = models.CASCADE
    )

    feed_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Define string """
        return self.feed_text
