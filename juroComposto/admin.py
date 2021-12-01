from django.contrib import admin

from .models import igpm

class IgpmAdmin(admin.ModelAdmin):
    list_display = ['data', 'taxa']
    ordering = ['data']
    pass
admin.site.register(igpm, IgpmAdmin)

admin.site.site_header = 'Freicali administration'
