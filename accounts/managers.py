
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, full_name, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username.')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, full_name, password):
        user = self.create_user(username, email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
