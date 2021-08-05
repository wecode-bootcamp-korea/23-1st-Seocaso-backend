from django.urls import path

from likes.views import CafeLikeView, ReviewLikeView

urlpatterns = [
    path('/cafe/<int:cafe_id>', CafeLikeView.as_view()),
    path('/review/<int:review_id>', ReviewLikeView.as_view())
]