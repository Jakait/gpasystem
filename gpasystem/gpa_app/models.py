from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager, Permission,Group

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provide a valid email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_user(self, email= None, password = None, **etxra_fields):
        etxra_fields.setdefault('is_staff', True)
        etxra_fields.setdefault('is_superuser', False)

        return self. _create_user(email,password,**etxra_fields)
    def create_superuser(self, email= None, password = None, **etxra_fields):
        etxra_fields.setdefault('is_staff', True)
        etxra_fields.setdefault('is_superuser', True)

        return self. _create_user(email,password,**etxra_fields)



class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(blank=True, default="",unique=True)
    username =  models.CharField(max_length=66, blank=True, null=True)
    firstname =  models.CharField(max_length=66, blank=True, null=True)
    last_name = models.CharField(max_length=66, blank=True, null=True)
    middle_name = models.CharField(max_length=66, blank=True, null=True)
    accesslevel = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = CustomUserManager()
    USERNAME_FIELD ="email"
    EMAIL_FIELD  = "email",
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username or self.email.split("@")[0]


  

    def __str__(self):
        return self.get_short_name()

    
class Lecturer(models.Model):
    Lec_no = models.CharField(max_length=10,blank=True, default="",unique=True)
    course_id  = models.ForeignKey('Course',on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey('User',on_delete=models.CASCADE, null=True,blank=True)
   

    def __str__(self):
        return self.user_id
    
class Student(models.Model):
    adm_no = models.CharField(max_length=10,blank=True, default="",unique=True)
    course_id  = models.ForeignKey('Course',on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey('User',on_delete=models.CASCADE, null=True,blank=True)
   

    def __str__(self):
        return self.user_id




class Semister(models.Model):
    sem_name = models.CharField(max_length=66, blank=True, null=True)
   


    def __str__(self):
        return  self.sem_name






class Exam(models.Model):
    unit_id  = models.ForeignKey('Unit',on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey('Student',on_delete=models.CASCADE, null=True,blank=True)
    lecturer = models.ForeignKey('Lecturer',on_delete=models.CASCADE, null=True,blank=True)
    semister = models.ForeignKey('Semister',on_delete=models.CASCADE, null=True,blank=True)
    score = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.id



# unit
class Unit(models.Model):
    course_id  = models.ForeignKey('Course',on_delete=models.SET_NULL, null=True, blank=True)
    unit_name = models.CharField(max_length=66, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unit_name
    
class Course(models.Model):
    course_name = models.CharField(max_length=66, blank=True, null=True)
    course_code = models.CharField(max_length=10,blank=True, null = True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


