from django.urls import path

from cafes.views import ReviewView, ReviewRankingView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/review-ranking', ReviewRankingView.as_view())
]