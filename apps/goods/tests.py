from django.test import TestCase
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Good
from django.views.generic import View


class GoodView(View):
    def get(self, request):
        goods = Good.objects.all()
        good_list = serializers.serialize('json', goods)
        return HttpResponse(good_list, content_type='application/json')
        # return JsonResponse(good_list, safe=False)
