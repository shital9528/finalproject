from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self,username,password,**extra_field):
        if not username:
            raise ValueError('Username is required!!')
        user=self.model(username=username,**extra_field)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,password,**extra_field):
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_superuser',True)
        return self.create_user(username,password,**extra_field)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = "username"
    objects = UserManager()



class Movie(models.Model):
    movie_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    director=models.CharField(max_length=200)
    image=models.CharField(max_length=1000)
    genre=models.CharField(max_length=200)
    duration=models.IntegerField()
    language=models.CharField(max_length=100)
    releasedate=models.DateField()


class Theater(models.Model):
    theater_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    pincode=models.CharField(max_length=50)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theater')
    timing=models.TimeField()


class Seat(models.Model):
    number=models.CharField(max_length=5)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='smovie')
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='stheater')
    available=models.BooleanField(default=True)
    price=models.IntegerField()


class Booking(models.Model):
    booking_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='buser')
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='bmovie')
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='btheater')
    seats=models.ManyToManyField(Seat)
    total_cost=models.FloatField(default=0.00)