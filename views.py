from django.shortcuts import render
from .models import AddBook
from .forms import BookForm
from django.contrib import messages
from django.db import connection
from django.core.paginator import Paginator
from django.http import JsonResponse

def add_books(request):
    saved = False
    
    with connection.cursor() as cursor:
        cursor.execute("Select * from example_addbook")
        books = cursor.fetchall()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['book_id']
            book_name = form.cleaned_data['title']
            select_query = "Select * from example_addbook where book_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(select_query, [id])
                existing_book = cursor.fetchone()

            if not existing_book:
                insert = "Insert into example_addbook (book_id, title) values (%s, %s)"
                with connection.cursor() as cursor:
                    cursor.execute(insert, [id, book_name]) 
                    connection.commit()
                saved = True
                data = {'book_id': id, 'title': book_name}
                return JsonResponse(data)
            
            else:
                messages.warning(request, 'Book already exists with the same details.')
                return JsonResponse({'error': 'Book already exists.'}, status=400)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    form = BookForm()
    return render(request, 'sample.html', {'form': form, 'saved': saved, 'books': books})



def get_books(request):
    searchtitle = request.GET.get('searchtitle', '')
    if searchtitle:
        search_query = "SELECT * FROM example_addbook WHERE title LIKE %s"
        with connection.cursor() as cursor:
            cursor.execute(search_query, ['%' + searchtitle + '%'])
            books = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM example_addbook")
            books = cursor.fetchall()
    

    data = [{'book_id': book[1], 'title': book[2]} for book in books]
    return JsonResponse({'books': data})
