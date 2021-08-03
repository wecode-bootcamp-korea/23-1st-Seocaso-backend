from django.db                 import models
from django.db.models.deletion import CASCADE

class Review(models.Model):
    content           = models.CharField(max_length=500)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True, null=True)
    user              = models.ForeignKey('users.user', on_delete=CASCADE)
    cafe              = models.ForeignKey('cafes.cafe', on_delete=CASCADE)
    comment_on_review = models.ForeignKey('self', on_delete=CASCADE, null=True)

    class Meta:
        db_table = 'reviews'