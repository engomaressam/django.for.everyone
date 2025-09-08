from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Make, Auto

@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'update_link')
    search_fields = ('name',)

    def update_link(self, obj):
        url = reverse('admin:autos_make_change', args=[obj.pk])
        return format_html('<a href="{}">Update</a>', url)
    update_link.short_description = 'Update'

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'make', 'owner', 'mileage', 'updated_at')
    list_filter = ('make',)
    search_fields = ('nickname', 'comments')
