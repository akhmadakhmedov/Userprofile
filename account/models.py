from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	first_name 				= models.CharField(max_length=30, verbose_name="Имя", default="")
	second_name 			= models.CharField(max_length=30, verbose_name="Фамилия", default="")
	email 					= models.EmailField(max_length=60, unique=True, verbose_name="Эл. адрес")
	username 				= models.CharField(max_length=30, unique=True, verbose_name='Логин')
	date_joined				= models.DateTimeField(auto_now_add=True, verbose_name="Дата присоединения")
	last_login				= models.DateTimeField(auto_now=True, verbose_name="Дата последнего входа")
	is_admin				= models.BooleanField(default=False, verbose_name='Админ')
	is_active				= models.BooleanField(default=True, verbose_name='Активен')
	is_staff				= models.BooleanField(default=False, verbose_name='Персонал')
	is_superuser			= models.BooleanField(default=False, verbose_name='Суперпользователь')


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
