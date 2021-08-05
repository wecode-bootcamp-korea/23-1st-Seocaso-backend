from django.db import models

class User(models.Model):
    email     = models.CharField(max_length=100, unique=True)
    password  = models.CharField(max_length=500)
    nickname  = models.CharField(max_length=45)
    image_url = models.URLField(max_length=1000, null=True)

    class Meta:
        db_table = 'users'
