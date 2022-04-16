from rest_framework import serializers
from .models import Vote_card , Stock_ticker , Experation_date


class Vote_card_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vote_card
        fields = "__all__"


class Ticker_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_ticker
        fields = "__all__"


class ExperationDate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Experation_date
        fields = "__all__"


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Experation_date
        fields = "__all__"

