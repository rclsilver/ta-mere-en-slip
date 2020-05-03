from backend import models
from django.contrib import admin


class ActionAdmin(admin.ModelAdmin):
    fields = [ 'text' ]
    list_display = [ 'text' ]


class CharacterAdmin(admin.ModelAdmin):
    fields = [ 'text' ]
    list_display = [ 'text' ]


admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.Character, CharacterAdmin)
