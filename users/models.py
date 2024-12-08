from django.db import models

class User(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    username = models.TextField()
    reg_date = models.TextField()
    last_act = models.TextField()

class Percentage(models.Model):
    name = models.TextField(primary_key=True)
    percent = models.IntegerField()

class ContestPerc(models.Model):
    uid = models.TextField()
    percent = models.FloatField()
    cid = models.IntegerField()
    link = models.TextField()
    is_done = models.BooleanField()

class CheckingDatas(models.Model):
    link = models.TextField()
    token = models.TextField()
    ltype = models.TextField()