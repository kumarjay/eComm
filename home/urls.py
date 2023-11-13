from django.urls import path
from home.views import index, category_index

urlpatterns = [
    
    path('', index, name='index'),
    path('<slug>/', category_index, name="category_index")
]