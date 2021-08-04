from django.urls import path

from ratings.views import StarRatingView

urlpatterns = [
    path('/<int:cafe_id>', StarRatingView.as_view()),
]