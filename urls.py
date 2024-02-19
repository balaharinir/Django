from django.contrib import admin
from django.urls import path
from example import views

urlpatterns = [
    path('', views.add_book, name='default_view'),
    
     path('add_book', views.add_book, name='add_book'),
    path('get_books/', views.get_books, name='get_books'),
    path('admin/', admin.site.urls)
]
