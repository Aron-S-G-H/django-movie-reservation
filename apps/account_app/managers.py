from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')
        if not password:
            raise ValueError("User must have a password")
        if not email:
            raise ValueError('User must have a email address')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)  # required for supporting multiple databases
        return user

    def create_superuser(self, first_name, last_name, email, phone, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
