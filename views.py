from django.shortcuts import render
from .models import AddBook
from .forms import BookForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import connection

def index(request):
    saved = False
    searchtitle = request.GET.get('searchtitle', '')
    

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['book_id']
            book_name = form.cleaned_data['title']
            select_query = "Select * from example_addbook where book_id = %s and title = %s"
            with connection.cursor() as cursor:
                cursor.execute(select_query, [id, book_name])
                existing_book = cursor.fetchone()

            if not existing_book:
                insert = "Insert into example_addbook (book_id, title) values (%s, %s)"
                with connection.cursor() as cursor:
                    cursor.execute(insert, [id, book_name]) 
                saved = True
                connection.commit()
            else:
                messages.warning(request, 'Book already exists with the same details.')

    if searchtitle:
        search = "Select * from example_addbook where title like %s"
        with connection.cursor() as cursor:
            cursor.execute(search, ['%' + searchtitle + '%'])
            books = cursor.fetchall()
    else:
        search = "SELECT * FROM example_addbook"
        with connection.cursor() as cursor:
            cursor.execute(search)
            books = cursor.fetchall()

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    form = BookForm()
    return render(request, 'sample.html', {'form': form, 'saved': saved, 'books': books, 'searchtitle': searchtitle})
