from django.urls import path

from cafes.views import ReviewView, CommentOnReviewView, MenuView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('/<int:cafe_id>/menus', MenuView.as_view())
]
