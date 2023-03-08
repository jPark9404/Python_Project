from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    content = models.TextField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)
