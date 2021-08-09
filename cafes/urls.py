from django.urls import path

from cafes.views import ReviewView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view())
]