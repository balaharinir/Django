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
    sort = request.GET.get('sort', '')
    page_number = request.GET.get('page','')
    params = []

    if searchtitle:
        search = "Select * from example_addbook where title like %s"
        params.append('%' + searchtitle + '%')
    else:
        search = "select * from example_addbook"

    if sort == 'desc':
        sorting = " order by title desc"
    elif sort == 'asc':
        sorting = " order by title "
    else:
        sorting = ""

    query = search + sorting
    
    limit = 10  
    offset = (int(page_number) - 1) * limit if page_number else 0
    pagination = query + " limit %s offset %s"
    params.append(limit)
    params.append(offset)

    with connection.cursor() as cursor:
        cursor.execute(pagination, params)
        books = cursor.fetchall()

    data = [{'book_id': book[1], 'title': book[2]} for book in books]

    
    return JsonResponse({'books': data})
