from django.db                 import models

class CafeLike(models.Model):
    user = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True)
    cafe = models.ForeignKey('cafes.cafe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cafe_likes'

class ReviewLike(models.Model):
    user   = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True)
    review = models.ForeignKey('reviews.review', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_likes'

