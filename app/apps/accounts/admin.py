from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.accounts.models import Account


@admin.register(Account)
class CustomAdminClass(ModelAdmin):
    pass
