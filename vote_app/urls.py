from django.urls import path
from django.http import HttpResponse , JsonResponse
from . import views
from requests import get
from json import load


# UPDATED LIST OF STOCKS
url = "https://dumbstockapi.com/stock?exchanges=NASDAQ"


urlpatterns = [
    path("" , lambda request : HttpResponse("welcome!") ),

    path("api/build", lambda request : JsonResponse( get(url).json() , safe=False) ),
    path("api/build_internal", lambda request : JsonResponse(load(open('stocks.json')),safe=False )),

    path("api/votes" , views.all_votes ),
    path("api/tickers" , views.all_stocks ),

    path("api/tickers/<str:ticker>" , views.ticker_details ),
    path("api/votes/<str:ticker>" , views.vote_card_details ),

    path("api/vote_experation_date" , views.expiration_date ),

    path("api/votes/<str:ticker>/up" , views.up_vote ),
    path("api/votes/<str:ticker>/down" , views.down_vote ),

    path("api/tickers/<str:ticker>/meme" , views.ticker_meme ),

]
