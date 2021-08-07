from django.urls import path

from cafes.views import CafeDetailView

urlpatterns = [
    path('/<int:cafe_id>', CafeDetailView.as_view()),
] 