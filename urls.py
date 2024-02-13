
from django.contrib import admin
from django.urls import path
from example import views

urlpatterns = [
    
    path('', views.add_books, name='default_view'),
    path('add_books/', views.add_books, name='add_books'),
    path('get_books/', views.get_books, name='get_books'),


    path('admin/', admin.site.urls)
    
]
