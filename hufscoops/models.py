from django.db import models
from django.utils import timezone


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    cafe_name = models.CharField(max_length=30, default="")
    time = models.CharField(max_length=30, default="")
    menu = models.CharField(max_length=100, default="")
    is_new = models.BooleanField(default=False)

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    cafe_name = models.CharField(max_length=30, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cafe_name + '\t\t\t시간 : ' + str(self.timestamp)