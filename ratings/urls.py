from django.urls import path

from ratings.views import RatingCountView

urlpatterns = [
    path('/count', RatingCountView.as_view())
]