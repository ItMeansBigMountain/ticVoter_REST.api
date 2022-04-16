from django.shortcuts import render
from django.http  import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 




from .models import Vote_card , Stock_ticker , Experation_date , Users_Voted
from .serializers import Vote_card_Serializer , Ticker_Serializer , ExperationDate_Serializer , User_Serializer



import requests
import random






# DISPLAY ALL OBJECTS

# ROUTE: "api/votes"
@api_view(['GET', 'POST'])
def all_votes(request):
    # FETCH DATA BASE
    if request.method == "GET":
        votes = Vote_card.objects.all()
        serializer = Vote_card_Serializer(votes , many=True)
        return Response( serializer.data  )
    
    # RECIEVES JSON POST REQUEST.data
    elif request.method == "POST":
        serializer =  Vote_card_Serializer(data=request.data) 
        
        # VALIDATE
        if serializer.is_valid():
            serializer.save()
            return Response( request.data , status=status.HTTP_201_CREATED )
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_401_UNAUTHORIZED)


# ROUTE: "api/tickers"
@api_view(['GET', 'POST'])
def all_stocks(request):
    # FETCH DATA BASE
    if request.method == "GET":
        stocks = Stock_ticker.objects.all()
        serializer = Ticker_Serializer(stocks , many=True)
        return Response( serializer.data  )
    
    # RECIEVES JSON POST REQUEST.data
    elif request.method == "POST":
        serializer =  Ticker_Serializer(data=request.data) 
        
        # VALIDATE
        if serializer.is_valid():
            serializer.save()
            return Response( request.data , status=status.HTTP_201_CREATED )
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_401_UNAUTHORIZED)









# DISPLAY INDIVISUAL OBJECT

# ROUTE: "api/tickers/<str:ticker>"
@api_view(['GET', 'PUT' , 'DELETE'])
def ticker_details(request , ticker):
    ticker = ticker.upper()
    # VALIDATE request
    try:
        ticker = Stock_ticker.objects.filter(ticker=ticker).last()
    except Stock_ticker.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response( str(e) ,status=status.HTTP_404_NOT_FOUND)
    

    if request.method == "GET":
        serializer = Ticker_Serializer(ticker)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

    elif request.method == "PUT":
        serializer =  Ticker_Serializer(ticker , data = request.data) 
        # VALIDATE serialization
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data , status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_406_NOT_ACCEPTABLE)


    elif request.method == "DELETE":
        ticker.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


# ROUTE: "api/votes/<str:ticker>"
@api_view(['GET', 'PUT' , 'DELETE'])
def vote_card_details(request , ticker):
    ticker = ticker.upper()
    # VALIDATE request
    try:

        vote = Vote_card.objects.filter(ticker=ticker).last()
        if not vote.experation.last() == Experation_date.objects.last():
            null_data = {
                'id' : None  ,
                'ticker' :  vote.ticker,
                'up_vote' : 0,
                'down_vote' : 0,
                'date' : None,
                'experation' : Experation_date.objects.last().date,
                'users_vote' : None
            }
            return JsonResponse(null_data)


    except Vote_card.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response( str(e) ,status=status.HTTP_404_NOT_FOUND)
    

    if request.method == "GET":
        serializer = Vote_card_Serializer(vote)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

    elif request.method == "PUT":
        serializer =  Vote_card_Serializer(vote , data = request.data) 
        # VALIDATE serialization
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data , status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response( serializer.data , status=status.HTTP_406_NOT_ACCEPTABLE)


    elif request.method == "DELETE":
        vote.delete()
        return Response(status=status.HTTP_202_ACCEPTED)






# EXPERATION DATE

# ROUTE: "api/vote_experation_date"
@api_view(['GET'])
def expiration_date(request):
    experation = Experation_date.objects.last()
    serializer = ExperationDate_Serializer(experation)
    return Response( serializer.data , status=status.HTTP_200_OK)









# UP VOTE / DOWN VOTE

# ROUTE: "api/votes/<str:ticker>/up"
@api_view(['POST'])
def up_vote(request , ticker):
    ticker = ticker.upper()

    try:
        # USER MODEL
        user_data = request.data['user']
        user_metrics = [
            'uid',
            'email',
            'emailVerified',
            'isAnonymous',
            'createdAt',
        ]
        user_dictionary  = { i : user_data[i] for i in user_metrics if user_data[i] != 'None'  }
        user_object = Users_Voted.objects.get_or_create(**user_dictionary)
        user_object.save() 
    except:
        Response( "Invalid Request Data" , status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)


    t = Stock_ticker.objects.filter(ticker=ticker).last()
    # someone voted already...
    if t:
        vote = t.history.last()
        # check if votes are current
        if vote and vote.experation.last() == Experation_date.objects.last():
            # check if user already voted
            if user_object[0] not in vote.users_voted.all():
                vote.up_vote += 1
                vote.save()
                vote.users_voted.add(user_object[0])
            else: return Response( "Already voted!" , status=status.HTTP_403_FORBIDDEN)
        else:
            # votes are not current
            vote = Vote_card( ticker=ticker, up_vote=1, down_vote=0 )
            vote.save()
            vote.users_voted.add(user_object[0])
            vote.experation.add(Experation_date.objects.last())
            t.history.add(vote)
    else:
        # first time stock was voted on in the database
        vote = Vote_card( ticker=ticker, up_vote=1, down_vote=0 )
        vote.save()
        vote.experation.add(Experation_date.objects.last())
        vote.save()
        vote.users_voted.add(user_object[0])
    
        t = Stock_ticker( ticker=ticker )
        t.save()
        t.history.add(vote)
    
    serializer = Vote_card_Serializer(vote)
    return Response( serializer.data , status=status.HTTP_202_ACCEPTED)



# ROUTE: "api/votes/<str:ticker>/down"
@api_view(['POST'])
def down_vote(request , ticker):
    ticker = ticker.upper()

    try:
        # USER MODEL
        user_data = request.data['user']
        user_metrics = [
            'uid',
            'email',
            'emailVerified',
            'isAnonymous',
            'createdAt',
        ]
        user_dictionary  = { i : user_data[i] for i in user_metrics if user_data[i] != 'None'  }
        user_object = Users_Voted.objects.get_or_create(**user_dictionary)
        user_object.save() 
    except:
        Response( "Invalid Request Data" , status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)


    t = Stock_ticker.objects.filter(ticker=ticker).last()
    # someone voted already...
    if t:
        vote = t.history.last()
        # check if votes are current
        if vote and vote.experation.last() == Experation_date.objects.last():
            # check if user already voted
            if user_object[0] not in vote.users_voted.all():
                vote.down_vote += 1
                vote.save()
                vote.users_voted.add(user_object[0])
            else: return Response( "Already voted!" , status=status.HTTP_403_FORBIDDEN)
        else:
            # votes are not current
            vote = Vote_card( ticker=ticker, up_vote=0, down_vote=1 )
            vote.save()
            vote.users_voted.add(user_object[0])
            vote.experation.add(Experation_date.objects.last())
            t.history.add(vote)
    else:
        # first time stock was voted on in the database
        vote = Vote_card( ticker=ticker, up_vote=0, down_vote=1 )
        vote.save()
        vote.experation.add(Experation_date.objects.last())
        vote.save()
        vote.users_voted.add(user_object[0])
    
        t = Stock_ticker( ticker=ticker )
        t.save()
        t.history.add(vote)
    
    serializer = Vote_card_Serializer(vote)
    return Response( serializer.data , status=status.HTTP_202_ACCEPTED)









# ROUTE: "api/tickers/<str:ticker>/meme"
@api_view(['GET'])
def ticker_meme(request, ticker):

    # fetch ticker stock data
    alphavantage_api = '  RYZYYUICAFR0M05R'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&interval=5min&apikey={alphavantage_api}'
    r = requests.get(url)
    data = r.json()


    # generate meem
    data['meme'] = memeGeneration(  str(ticker) ,  str(data)  )
    

    return Response( data['meme'] , status=status.HTTP_200_OK)



def memeGeneration(name , info):
    #login
    username = 'oyamaMotivation'
    password = 'paper40gap'

    #fetch all memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data if image['box_count'] < 3]


    # Identify meme
    text0 = name
    text1 = info
    id = random.randint(0, len(images) - 1 )



    #generated meme
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':text0,
        'text1':text1
    }
    response = requests.request('POST',URL,params=params).json()
    imageURL = response['data']['url']
    return imageURL

