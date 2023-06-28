from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.add_tag, name='add_tag'),
    path('author/', views.add_author, name='add_author'),
    path('quote/', views.add_quote, name='add_quote'),
]
