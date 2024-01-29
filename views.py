from django.shortcuts import render
from .models import AddBook
from .forms import BookForm
from django.contrib import messages
from django.db import connection
from django.core.paginator import Paginator
from django.http import JsonResponse

def get_books(request):
    saved = False
    searchtitle = request.GET.get('searchtitle', '')
    sort = request.GET.get('sort', '')
    page = int(request.GET.get('page', 1))

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




    if searchtitle:
        search = "Select * from example_addbook where title like %s"
        with connection.cursor() as cursor:
            cursor.execute(search, ['%' + searchtitle + '%'])
            books = cursor.fetchall()
        if sort == 'desc':
            with connection.cursor() as cursor:
                cursor.execute("Select * from example_addbook order by title desc")
                books = cursor.fetchall()
            
        elif sort == 'asc':
            with connection.cursor() as cursor:
                cursor.execute("Select * from example_addbook order by title")
                books = cursor.fetchall()

    else:
        search = "Select * from example_addbook"
        with connection.cursor() as cursor:
            cursor.execute(search)
            books = cursor.fetchall()
      
        if sort == 'desc':
            with connection.cursor() as cursor:
                cursor.execute("Select * from example_addbook order by title desc")
                books = cursor.fetchall()
            
        elif sort == 'asc':
            with connection.cursor() as cursor:
                cursor.execute("Select * from example_addbook order by title")
                books = cursor.fetchall()
            
    paginator = Paginator(books, 10)
    books = paginator.get_page(page)
    
    form = BookForm()

    return render(request, 'sample.html', {'form': form, 'saved': saved, 'books': books, 'searchtitle': searchtitle, 'page': page})
