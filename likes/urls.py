from django.urls import path

from likes.views import CafeLikeView, ReviewLikeView

urlpatterns = [
    path('/<int:cafe_id>/cafe', CafeLikeView.as_view()),
    path('/<int:review_id>/review', ReviewLikeView.as_view())
]