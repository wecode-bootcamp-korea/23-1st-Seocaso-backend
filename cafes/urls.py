from django.urls import path

from cafes.views import ReviewView, CommentOnReviewView, SearchView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('', SearchView.as_view())
]
