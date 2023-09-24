from django.db import models


class User(models.Model):
    """ Пользователь системы """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    reg_date = models.DateTimeField(auto_now_add=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Event(models.Model):
    """ Событие """
    header = models.CharField(max_length=64)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    participants = models.ManyToManyField(User, related_name='events')

    def __str__(self):
        return self.header