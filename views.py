
from django.shortcuts import render
from .models import AddBook
from .forms import BookForm
from django.contrib import messages
from django.db import connection

from django.http import JsonResponse

import json

def add_book(request):
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
                return JsonResponse({'error': 'Book already exists.'}, status=400)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = BookForm()
        return render(request, 'sample.html', {'form': form, 'saved': saved, 'books': books})



def get_books(request):
    searchtitle = request.GET.get('searchtitle', '')
    sort = request.GET.get('sort', '')
    page_number = request.GET.get('page','1')
    params = []

    if searchtitle:
        search = "Select * from example_addbook where title like %s"
        searchCount = "Select count(*) from example_addbook where title like %s"
        params.append('%' + searchtitle + '%')
    else:
        search = "select * from example_addbook"
        searchCount = "select count(*) from example_addbook"

    ### Count
    with connection.cursor() as cursor:
        cursor.execute(searchCount, params)
        totalCount = cursor.fetchone()[0]

    print("Books Count --> " + str(totalCount))

    if sort == 'desc':
        sorting = " order by title desc"
    elif sort == 'asc':
        sorting = " order by title "
    else:
        sorting = ""

    query = search + sorting

    if page_number:
        page_number_int = int(page_number)
    else: 
        page_number_int = 1

    limit = 10  

    if totalCount > 0:
        total_pages = int(totalCount / limit) + 1
    else: 
        total_pages = 0

    if page_number_int <= 1:
        hasPrevious = False
    else:
        hasPrevious = True
    if page_number_int < total_pages:
        hasNext = True
    else:
        hasNext = False

    offset = (page_number_int - 1) * limit
    query = query + " limit %s offset %s"
    params.append(limit)
    params.append(offset)

    pagination = [{
            'totalCount': totalCount, 
            'page_number_int': page_number_int,
            'total_pages': total_pages,
            'hasPrevious': hasPrevious,
            'hasNext': hasNext,
            'offset': offset,
            'query': query,
    }]

    print("pagination ------------> " + json.dumps(pagination, indent=4))

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        books = cursor.fetchall()

    data = [{'book_id': book[1], 'title': book[2]} for book in books]
    
    return JsonResponse({'books': data, 'pagination' : pagination})
