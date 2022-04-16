import requests
from vote_app.models import Vote_card , Stock_ticker , Experation_date
from datetime import datetime
import json



      
def update_experation_model():
    
    # RESET DATE
    experation =  Experation_date.objects.create()

    # UPDATE STOCKS LIST
    with open("stocks.json" , 'w') as db:
        url = 'https://dumbstockapi.com/stock?exchanges=NASDAQ'
        db.write(  json.dumps(requests.get(url).json())   )


    print("RESTTING DATA")