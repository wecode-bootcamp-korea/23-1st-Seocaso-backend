from django.db                 import models
from django.db.models.deletion import CASCADE

class Cafe(models.Model):
    name           = models.CharField(max_length=100)
    address        = models.CharField(max_length=200)
    hours          = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=45)
    description    = models.CharField(max_length=500)
    main_image_url = models.URLField(max_length=1000)

    class Meta:
        db_table = 'cafes'

class Menu(models.Model):
    name      = models.CharField(max_length=45)
    price     = models.DecimalField(max_digits=10 ,decimal_places=2)
    image_url = models.URLField(max_length=1000)
    cafe      = models.ForeignKey('cafe', on_delete=CASCADE)

    class Meta:
        db_table = 'menus'

class CafeImage(models.Model):
    image_url = models.URLField(max_length=1000)
    cafe      = models.ForeignKey('cafe', on_delete=CASCADE)

    class Meta:
        db_table = 'cafe_images'