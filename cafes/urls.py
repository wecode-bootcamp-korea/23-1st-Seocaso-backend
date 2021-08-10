from django.urls import path

from cafes.views import ReviewView, CommentOnReviewView, UserCafeListView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('/user/<int:user_id>', UserCafeListView.as_view())
]