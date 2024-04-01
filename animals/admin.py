from django.contrib import admin
from animals.models import Animal

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'name', 'specie', 'breed', 'service')
    search_fields = ('name',)


admin.site.register(Animal, AnimalAdmin)
