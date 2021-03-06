from django.db                 import models

class Cafe(models.Model):
    name           = models.CharField(max_length=20)
    address        = models.CharField(max_length=200)
    business_hours = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=20)
    description    = models.CharField(max_length=500)
    main_image_url = models.URLField(max_length=1000)

    class Meta:
        db_table = 'cafes'

class Menu(models.Model):
    name      = models.CharField(max_length=45)
    price     = models.DecimalField(max_digits=10 ,decimal_places=2)
    image_url = models.URLField(max_length=1000)
    cafe      = models.ForeignKey('cafe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'menus'

class CafeImage(models.Model):
    image_url = models.URLField(max_length=1000)
    cafe      = models.ForeignKey('cafe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cafe_images'

class Collection(models.Model):
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'collections'

class CafeCollection(models.Model):
    cafe       = models.ForeignKey('cafe', on_delete=models.CASCADE)
    collection = models.ForeignKey('cafecollection', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cafe_collections'