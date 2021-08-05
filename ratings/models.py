from django.db                 import models

class StarRating(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    user  = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True)
    cafe  = models.ForeignKey('cafes.cafe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'star_ratings'
