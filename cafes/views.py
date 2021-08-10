import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from reviews.models import Review
from cafes.models   import Cafe
from utils          import log_in_confirm

class ReviewView(View):
    @log_in_confirm
    def post(self, request, cafe_id):
        try:
            if Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id).exists():
                return JsonResponse({'MESSAGE' : 'REVIEW_ALREADY_EXIST'}, status=400)

            data    = json.loads(request.body)
            cafe    = Cafe.objects.get(id=cafe_id)
            content = data['content']

            if not content:
                return JsonResponse({'MESSAGE' : 'EMPTY_CONTENT'}, status=400)

            Review.objects.create(
                user    = request.user,
                cafe    = cafe,
                content = content
            )
            return JsonResponse({'MESSAGE' : 'REVIEW_CREATED'}, status=201)

        except KeyError:
            return  JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'JSON_DECODE_ERROR'}, status=400)

    @log_in_confirm
    def delete(self, request, cafe_id):
        review = Review.objects.filter(cafe_id=cafe_id, user_id=request.user.id)
        if not review.exists():
            return JsonResponse({'MESSAGE' : 'REVIEW_DOES_NOT_EXIST'}, status=400)

        review.delete()
        return JsonResponse({'MESSAGE' : 'REVIEW_DELETED'}, status=204)
    
class CommentOnReviewView(View):
    @log_in_confirm
    def post(self, request, review_id):
        data    = json.loads(request.body)

        if not Review.objects.filter(id=review_id).exists(): 
            return JsonResponse({'MESSAGE':'REVIEW_DOES_NOT_EXIST'}, status=404)
            
        cafe_id = Review.objects.get(id=review_id).cafe_id

        Review.objects.create(
            content              = data['content'],
            cafe_id              = cafe_id,
            comment_on_review_id = review_id,
            user                 = request.user
    )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

class SearchView(View):
    def get(self, request):
        search_keyword = request.GET.get('q', '')

        cafe_results = Cafe.objects.filter(name__icontains=search_keyword)[:14]
        address_results = Cafe.objects.filter(address__icontains=search_keyword)[:14]

        if search_keyword:
            
            cafe_name_results = [{
                'id'     : cafe_result.id,
                'image'  : cafe_result.main_image_url,
                'name'   : cafe_result.name,
                'address': cafe_result.address
            }for cafe_result in cafe_results
            ]

            address_search_results = [{
                'id'     : address_result.id,
                'image'  : address_result.main_image_url,
                'name'   : address_result.name,
                'address': address_result.address
            } for address_result in address_results
            ]

        return JsonResponse({
            'cafe_name_results'     : cafe_name_results,
            'address_search_results': address_search_results
            }, status=200)
