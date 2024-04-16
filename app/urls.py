from django.contrib import admin
from django.urls import path
from animals.views import animal_view, animal_create,animal_delete, animal_update
from django.urls import path
from accounts.views import registro_api,login_api
from product.views import list_products,create_product,update_product,delete_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('animal/list/', animal_view),  
    path('animal/save/', animal_create),
    path('animal/delete/', animal_delete), 
    path('animal/update/',animal_update), 
    path('register/', registro_api),
    path('login/', login_api),
    path('product/list/', list_products),
    path('product/save/', create_product),
    path('product/update/',update_product),
    path('product/delete/', delete_product),
]
