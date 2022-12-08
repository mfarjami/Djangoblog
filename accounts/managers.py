
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self, username, email, full_name=None, password=None):
		# if not email:
		# 	raise ValueError('user must have email')

		if not username:
			raise ValueError('user must have username')

		user = self.model(username=username, email=self.normalize_email(email), full_name=full_name)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, full_name, password):
		user = self.create_user(username, email, full_name, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

    # def _create_user(self, username, email, password, **extra_fields):
    #     """
    #     Create and save a user with the given username, email, and password.
    #     """
    #     if not email:
    #         raise ValueError('user must have email')

    #     if not username:
    #         raise ValueError('The given username must be set')
    #     email = self.normalize_email(email)
    #     user = self.model(username=username, email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_user(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(username, email, password, **extra_fields)

    # def create_superuser(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self._create_user(username, email, password, **extra_fields)