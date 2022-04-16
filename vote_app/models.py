from django.db import models
from datetime import datetime



class Experation_date(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date}"



class Users_Voted(models.Model):
    uid = models.CharField(max_length=100 , default=None)
    email = models.EmailField( default=None )
    emailVerified = models.BooleanField( default=None )
    isAnonymous = models.BooleanField(default=None)
    createdAt = models.IntegerField(default=None)
    def __str__(self):
        if self.email: return f"{self.email} "
        else: return self.uid









class Vote_card(models.Model):
    ticker = models.CharField(max_length=10)
    up_vote = models.IntegerField()
    down_vote = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    experation = models.ManyToManyField(Experation_date , default=None)
    users_voted = models.ManyToManyField(Users_Voted , default=None)

    def __str__(self):
        experation = self.experation.last().date.date()
        return f"{self.ticker} | {self.up_vote}:{self.down_vote} | {experation}"






class Stock_ticker(models.Model):
    ticker = models.CharField(max_length=10)
    history = models.ManyToManyField(Vote_card , default=None)
    # date = self.history.latest().date

    def __str__(self):
        experation = self.history.last().date.date()
        return f"{self.ticker} | {self.history.count()} | {experation}"



