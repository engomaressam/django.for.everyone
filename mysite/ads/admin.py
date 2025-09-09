from django.contrib import admin
from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'text')
    readonly_fields = ('created_at', 'updated_at')