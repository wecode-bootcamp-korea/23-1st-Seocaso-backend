import json
from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View

from ratings.models import StarRating
from users.models   import User
from cafes.models   import Cafe
from utils          import LoginConfirm

class StarRatingView(View):
    @LoginConfirm
    def post(self, request, cafe_id):
        try:
            data = json.loads(request.body)

            user = request.user

            if not Cafe.objects.filter(id=cafe_id).exists():
                return JsonResponse({'MESSAGE':'CAFE_DOES_NOT_EXIST'}, status=401)
            
            cafe = Cafe.objects.get(id=cafe_id)

            if StarRating.objects.filter(user_id=user.id, cafe_id=cafe_id).exists():
                
                star, flag = StarRating.objects.get_or_create(score=data['score'], user_id=user.id, cafe_id=cafe.id)

                if not flag:
                    star.delete()
                if flag and (star.score != data['score']):
                    star.score = data['score']
                else:
                    return JsonResponse({'MESSAGE':'CREATED'}, status=201) 
                
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        
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
