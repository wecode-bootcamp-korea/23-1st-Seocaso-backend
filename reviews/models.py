from django.db                 import models

class Review(models.Model):
    content           = models.CharField(max_length=500)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    user              = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True)
    cafe              = models.ForeignKey('cafes.cafe', on_delete=models.CASCADE)
    comment_on_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'reviews'