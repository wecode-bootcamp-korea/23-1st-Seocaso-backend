from django.urls import path

from users.views   import SignupView, SigninView
from reviews.views import ReviewView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
]