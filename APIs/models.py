from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField

class Users(AbstractBaseUser):
    username = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        db_table = 'Users'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email','name','password') 
    
    def __str__(self):
        return self.name


class SportList(models.Model):
    name = models.CharField(max_length = 20, primary_key=True)
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    category = models.CharField(max_length=20)

class favSports(models.Model):    
    name = models.CharField(max_length=50, unique=True, primary_key= True)
    sport = ArrayField(models.CharField(max_length=50))

class brodacastMessages(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0
        ACCEPTED = 1
    category = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    players = models.IntegerField()  
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    accepted_by = ArrayField(models.CharField(max_length=20, blank=True, null=True),null=True)    
    status = models.IntegerField(choices=Status.choices, default=0)

class teamList(models.Model):
    team_id = models.IntegerField(unique=True, primary_key=True)
    team_name = models.CharField(unique=True)
    owner = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    max_members = models.IntegerField()
    members = ArrayField(models.CharField(max_length=20, blank=True, null=True))
    join_requests = ArrayField(models.CharField(max_length=20,blank=True, null=True),null=True)
    match_requests = ArrayField(models.CharField(max_length=20,blank=True, null=True),null=True)
    match_schedules = ArrayField(models.CharField(max_length=20,blank=True, null=True),null=True)