from django.db                 import models
from django.db.models.deletion import CASCADE

class CafeLike(models.Model):
    user = models.ForeignKey('users.user', on_delete=CASCADE)
    cafe = models.ForeignKey('cafes.cafe', on_delete=CASCADE)

    class Meta:
        db_table = 'cafe_likes'

class ReviewLike(models.Model):
    user   = models.ForeignKey('users.user', on_delete=CASCADE)
    review = models.ForeignKey('reviews.review', on_delete=CASCADE)

    class Meta:
        db_table = 'review_likes'

