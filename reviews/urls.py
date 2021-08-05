from django.urls import path

from reviews.views import ReviewView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view())
]