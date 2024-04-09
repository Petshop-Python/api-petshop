from django.contrib import admin
from django.urls import path
from animals.views import animal_view, animal_create,animal_delete, animal_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('animal/list/', animal_view),  
    path('animal/save/', animal_create),
    path('animal/delete/', animal_delete), 
    path('animal/update/',animal_update), 
]
