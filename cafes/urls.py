from django.urls import path

from cafes.views import ReviewRankingView

urlpatterns = [
    path('/review-ranking', ReviewRankingView.as_view())
]
