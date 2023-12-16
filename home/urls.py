from django.urls import path
from home.views import index, category_index, about

urlpatterns = [
    
    path('', index, name='index'),
    path('v2/<slug>/', category_index, name="category_index"),
    path('about/', about, name="about")
]