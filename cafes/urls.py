from django.urls import path

from cafes.views import RatingRankingView

urlpatterns = [
    path('/rating-ranking', RatingRankingView.as_view())
]