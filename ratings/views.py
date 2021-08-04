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

            user = User.objects.get(id=request.user.id)

            if not Cafe.objects.filter(id=cafe_id).exists():
                return JsonResponse({'MESSAGE':'CAFE_DOES_NOT_EXIST'}, status=401)
            else:
                cafe = Cafe.objects.get(id=cafe_id)

            if (StarRating.objects.filter(user_id=request.user.id, cafe_id=cafe_id).exists()):
                
                if StarRating.objects.filter(
                    user_id=request.user.id, cafe_id=cafe_id, score=data['score']
                    ).exists():
                    StarRating.objects.filter(
                        user_id=request.user.id, cafe_id=cafe_id, score=data['score']
                        ).delete()
                
                else:
                    duplicate_star = StarRating.objects.filter(user_id=request.user.id, cafe_id=cafe_id)
                    duplicate_star.update(score=data['score'])
                
            else:    
                StarRating.objects.create(
                    score = data['score'],
                    user  = user,
                    cafe  = cafe
                )
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
                    'cafe' : star_rating.cafe_id,
                    'user' : star_rating.user_id
                }
            )

        return JsonResponse({'result':results}, status=200)
