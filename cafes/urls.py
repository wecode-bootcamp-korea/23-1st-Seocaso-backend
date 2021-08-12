from django.urls import path

from cafes.views import ReviewView, RatingCountView, CommentOnReviewView, CafeListView, MenuView, StarRatingView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/rating-count', RatingCountView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('', CafeListView.as_view()),
    path('/<int:cafe_id>/menus', MenuView.as_view()),
    path('/<int:cafe_id>/star-rating', StarRatingView.as_view(), )
]
