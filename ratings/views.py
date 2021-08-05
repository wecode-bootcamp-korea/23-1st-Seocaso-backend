import json
from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View

from ratings.models import StarRating
from users.models   import User
from cafes.models   import Cafe
from utils          import log_in_confirm

class StarRatingView(View):
    @log_in_confirm
    def post(self, request, cafe_id):
        try:
            data = json.loads(request.body)
            
            user = request.user
            
            if not Cafe.objects.filter(id=cafe_id).exists():
                return JsonResponse({'MESSAGE':'CAFE_DOES_NOT_EXIST'}, status=401)
            
            star, flag = StarRating.objects.get_or_create(cafe_id=cafe_id, user_id=user.id)

            if not flag:
                if star.score == data['score']:
                    star.delete()
                    return JsonResponse({'MESSAGE' : 'SCORE_DELETED'}, status=200)

                else:
                    star.score = data['score']
                    star.save()
                    return JsonResponse({'MESSAGE' : 'SCORE_UPDATED'}, status=200)
            else:
                StarRating.objects.filter(cafe_id=cafe_id, user_id=user.id).update(score=data['score'])
                return JsonResponse({'MESSAGE' : 'SCORE_CREATED'}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)
    
    def get(self, request, cafe_id):
        
        star_ratings = StarRating.objects.filter(cafe_id=cafe_id)
        
        results = []
        
        for star_rating in star_ratings:
            results.append(
                {
                    'score': star_rating.score,
                    'cafe_id' : star_rating.cafe_id,
                    'user_id' : star_rating.user_id
                }
            )

        return JsonResponse({'result':results}, status=200)
