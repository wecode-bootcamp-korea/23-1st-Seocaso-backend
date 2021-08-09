from django.urls import path

from cafes.views import ReviewView, RatingRankingView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/rating-ranking', RatingRankingView.as_view())
]