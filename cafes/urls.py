from django.urls import path

from cafes.views import CafeView, ReviewView, RatingCountView, CommentOnReviewView,CafeListView, MenuView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/rating-count', RatingCountView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('', CafeListView.as_view()),
    path('/<int:cafe_id>/menus', MenuView.as_view()),
    path('/<int:cafe_id>/information', CafeView.as_view()),
]
