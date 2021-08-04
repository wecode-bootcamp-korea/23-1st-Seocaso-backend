from django.urls import path

from ratings.views import StarRatingView

urlpatterns = [
    path('/star_rating', StarRatingView.as_view()),
]