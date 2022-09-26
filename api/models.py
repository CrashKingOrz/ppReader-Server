from django.db import models


# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'User'


class Query(models.Model):
    id = models.AutoField(primary_key=True)
    open_id = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    content = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10240)

    class Meta:
        db_table = 'Query'


class Time(models.Model):
    id = models.AutoField(primary_key=True)
    open_id = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)

    class Meta:
        db_table = 'Time'
