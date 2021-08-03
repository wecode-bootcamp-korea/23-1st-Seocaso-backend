from django.db import models

class Cafe(models.Model):
    name                 = models.CharField(max_length=45)
    number               = models.CharField(max_length=45)
    address              = models.CharField(max_length=200)
    hours                = models.CharField(max_length=45)
    information          = models.CharField(max_length=500)
    background_image_url = models.URLField(max_length=1000, null=True)
    poster_url           = models.URLField(max_length=1000, null=True)

    class Meta:
        db_table = 'cafes'

class Menu(models.Model):
    name = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    image_url = models.URLField(max_length=1000)
    cafe = models.ForeignKey('cafe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'menus'


