from django.urls import path

<<<<<<< HEAD
from cafes.views import ReviewView, RatingCountView, CommentOnReviewView, CafeListView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/rating-count', RatingCountView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('', CafeListView.as_view())
=======
from cafes.views import ReviewView, CommentOnReviewView, MenuView

urlpatterns = [
    path('/<int:cafe_id>/review', ReviewView.as_view()),
    path('/<int:review_id>/comment', CommentOnReviewView.as_view()),
    path('/<int:cafe_id>/menus', MenuView.as_view())
>>>>>>> 2c076e5eb1e20a5640ec68ef46d81b49362ed229
]
