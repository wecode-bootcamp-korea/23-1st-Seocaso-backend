from django.urls import path

from ratings.views import StarRatingView

urlpatterns = [
    path('/{cafe_id}/star-rating', StarRatingView.as_view()),
]