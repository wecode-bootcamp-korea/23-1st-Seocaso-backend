from django.urls import path

from cafes.views import ReviewView, CafeListView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('', CafeListView.as_view())
]