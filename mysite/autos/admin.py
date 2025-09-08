from django.contrib import admin
from .models import Make, Auto

@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'make', 'owner', 'mileage', 'updated_at')
    list_filter = ('make',)
    search_fields = ('nickname', 'comments')
