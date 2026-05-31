from django.contrib import admin

from .models import BorrowRequest, Equipment

admin.site.register(Equipment)
admin.site.register(BorrowRequest)
