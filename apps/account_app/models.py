from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import CustomUserManager
from django.core.validators import EmailValidator, MinLengthValidator


class CustomUser(AbstractUser):
    # Override the 'username' field to remove it
    username = None

    email = models.EmailField(verbose_name='email address', unique=True, validators=[EmailValidator])
    phone = models.CharField(max_length=11, unique=True, verbose_name='phone', validators=[MinLengthValidator(11)])

    USERNAME_FIELD = "phone"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
