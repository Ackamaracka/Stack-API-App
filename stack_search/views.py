from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

class AnonMinThrottle(AnonRateThrottle):
     scope = 'anon_min'

class AnonDayThrottle(AnonRateThrottle):
     scope = 'anon_day'


def search_url(searchtable):
    search = "https://api.stackexchange.com/2.2/search/advanced?page="
    if searchtable['page']:
        search += searchtable['page']
    if searchtable['pagesize']:
        search += "&pagesize="+ searchtable['pagesize']
    if searchtable['fromdate']:
        search += "&fromdate="+ searchtable['fromdate']
    if searchtable['todate']:
        search += "&todate="+ searchtable['todate'] 
    if searchtable['order']:
        search += "&order="+ searchtable['order']
    if searchtable['mini']:
        search += "&min="+ searchtable['mini']
    if searchtable['maxi']:
        search += "&max="+ searchtable['maxi']
    if searchtable['sort']:
        search += "&sort="+ searchtable['sort']
    if searchtable['q']:
        search += "&q="+ searchtable['q']
    if searchtable['accepted']:
        search += "&accepted="+ searchtable['accepted']
    if searchtable['answers']:
        search += "&answers="+ searchtable['answers']
    if searchtable['body']:
        search += "&body="+ searchtable['body']
    if searchtable['closed']:
        search += "&closed="+ searchtable['closed']
    if searchtable['migrated']:
        search += "&migrated="+ searchtable['migrated']
    if searchtable['notice']:
        search += "&notice="+ searchtable['notice']
    if searchtable['nottaged']:
        search += "&nottagged="+ searchtable['nottaged']
    if searchtable['tagged']:
        search += "&tagged="+ searchtable['tagged']
    if searchtable['title']:
        search += "&title="+ searchtable['title']
    if searchtable['user']:
        search += "&user="+ searchtable['user']
    if searchtable['url']:
        search += "&url="+ searchtable['url']
    if searchtable['views']:
        search += "&views="+ searchtable['views']
    if searchtable['wiki']:
        search += "&wiki="+ searchtable['wiki']
    search += "&site=stackoverflow"
    
    response = requests.get(search)
    return response


class StackSearch(APIView):
    permission_classes = []
    throttle_classes = [AnonMinThrottle, AnonDayThrottle]

    @method_decorator(cache_page(60*60*2))
    def get(self, request):
        searchtable = {
            "page"      : request.GET.get("page", None),
            "pagesize"  : request.GET.get("pagesize", None),
            "fromdate"  : request.GET.get("fromdate", None),
            "todate"    : request.GET.get("todate", None),
            "order"     : request.GET.get("order", None),
            "mini"      : request.GET.get("min", None),
            "maxi"      : request.GET.get("max", None),
            "sort"      : request.GET.get("sort", None),
            "q"         : request.GET.get("q", None),
            "accepted"  : request.GET.get("accepted", None),
            "answers"   : request.GET.get("answers", None),
            "body"      : request.GET.get("body", None),
            "closed"    : request.GET.get("closed", None),
            "migrated"  : request.GET.get("migrated", None),
            "notice"    : request.GET.get("notice", None),
            "nottaged"  : request.GET.get("nottaged", None),
            "tagged"    : request.GET.get("tagged", None),
            "title"     : request.GET.get("title", None),
            "user"      : request.GET.get("user", None),
            "url"       : request.GET.get("url", None),
            "views"     : request.GET.get("views", None),
            "wiki"      : request.GET.get("wiki", None),
        }

        data = json.loads(search_url(searchtable).content)

        return Response(data, status=status.HTTP_200_OK)