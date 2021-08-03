from django.db                 import models
from django.db.models.deletion import CASCADE

class CommentOnReview(models.Model):
    content    = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    review     = models.ForeignKey('reviews.review', on_delete=CASCADE)

    class Meta:
        db_table = 'comments_on_reviews'
