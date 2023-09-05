from django.contrib import admin
from .models import User, Category, Bid, Listing, Transaction, Comments
# Register your models here.


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Transaction)
admin.site.register(Comments)