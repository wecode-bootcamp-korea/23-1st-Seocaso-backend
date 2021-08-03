from django.db                 import models
from django.db.models.deletion import CASCADE

class StarRating(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1)
    user  = models.ForeignKey('users.user', on_delete=CASCADE)
    cafe  = models.ForeignKey('cafes.cafe', on_delete=CASCADE)

    class Meta:
        db_table = 'star_ratings'
