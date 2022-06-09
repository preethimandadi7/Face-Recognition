from django.db import models

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    email = models.EmailField()
    officeId = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    face = models.TextField(max_length=200)
    userId = models.IntegerField()
    groupId = models.IntegerField()

class Groups(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    userId = models.IntegerField()