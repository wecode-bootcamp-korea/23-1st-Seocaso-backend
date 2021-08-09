from django.urls import path

from reviews.views import CommentOnReviewView

urlpatterns = [
    path('/<int:review_id>/comments', CommentOnReviewView.as_view())
] 