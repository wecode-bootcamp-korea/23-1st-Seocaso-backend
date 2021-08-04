from django.urls import path

from reviews.views import ReviewView

urlpatterns = [
    path('/<int:cafe_id>', ReviewView.as_view())
]