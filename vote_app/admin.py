from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Vote_card)
admin.site.register(Stock_ticker)
admin.site.register(Experation_date)
admin.site.register(Users_Voted)