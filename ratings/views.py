from django.http.response import JsonResponse
from django.views import View

from ratings.models import StarRating

class RatingCountView(View):
    def get(self, request):
        return JsonResponse({'RATINGS_COUNT' : StarRating.objects.count()}, status=200)