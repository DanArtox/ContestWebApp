from django.contrib import admin
from .models import Percentage, ContestPerc, User, CheckingDatas

# Register your models here.
admin.site.register(Percentage)
admin.site.register(ContestPerc)
admin.site.register(User)
admin.site.register(CheckingDatas)