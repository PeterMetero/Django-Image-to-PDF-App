from django.contrib import admin
from .models import ConversionLog

@admin.register(ConversionLog)
class ConversionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'image_count', 'created_at')
    search_fields = ('filename',)