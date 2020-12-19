from django.contrib import admin

from .models import Poem

class PoemAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_to', 'date_from', 'text')
    search_fields = ('name', 'author', 'text',)
    list_filter = ('author',)

admin.site.register(Poem, PoemAdmin)

