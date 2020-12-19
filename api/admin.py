from django.contrib import admin

from .models import Poem, Citate

class PoemAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_to', 'date_from', 'text')
    search_fields = ('name', 'author', 'text',)
    list_filter = ('author',)

class CitateAdmin(admin.ModelAdmin):
    list_display = ('line', 'lemmed_line', 'poem',)
    search_fields = ('line', 'lemmed_line',)
    list_filter = ('poem',)

admin.site.register(Poem, PoemAdmin)
admin.site.register(Citate, CitateAdmin)


