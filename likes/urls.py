from django.urls import path

from likes.views import CafeLikeView

urlpatterns = [
    path('/<int:cafe_id>/cafe', CafeLikeView.as_view())
]