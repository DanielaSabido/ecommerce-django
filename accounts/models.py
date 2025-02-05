from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
    #class para  el registro
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')
        if not username:
            raise ValueError('El usuario debe tener un username')
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        #para crear un password e ingresarlo en la bd
        user.set_password(password)
        user.save(using=self._db)
        return user

    #funcion para superuser
    def create_superuser(self,first_name,last_name,email,username,password):
        user= self.create_user(
        email=self.normalize_email(email),
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        )
        #valores como administrador
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True

    #para crear un superadmin e ingresarlo en la bd
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.CharField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)

    #declarar campos por defects de djangoproject
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #para que cuando loguee sea con el UserAttributeSimilarityValidator
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username','first_name','last_name']

    #
    objects=MyAccountManager()

    #el valor que se pinte para representar a cada usuario
    def __str__(self):
        return self.email

        #para indicar si tiene permisos de administrador
    def has_perm(self, perm, obj=None):
        return self.is_admin

    #darle acceso a los modulos
    def has_module_perms(self,add_label):
        return True
