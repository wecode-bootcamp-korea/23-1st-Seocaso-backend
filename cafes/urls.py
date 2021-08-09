from django.urls import path

from cafes.views import ReviewView, RatingCountView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/rating-count', RatingCountView.as_view()),
]