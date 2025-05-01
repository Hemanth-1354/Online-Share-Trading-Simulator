from django.contrib import admin
from .models import Profile, StockHolding, Transaction, Stock

admin.site.register(Profile)
admin.site.register(Transaction)
admin.site.register(Stock)
admin.site.site_header = "Stock Market Admin"
admin.site.site_title = "Stock Market Admin Portal"
admin.site.index_title = "Welcome to Stock Market Admin Portal"
admin.site.register(StockHolding)


# Register your models here.
