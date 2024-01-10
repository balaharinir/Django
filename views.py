from django.shortcuts import render
from .models import AddBook
from .forms import BookForm
from django.contrib import messages


def index(request):
    saved = False
    searchtitle = request.GET.get('searchtitle', '')
    

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['book_id']
            book_name = form.cleaned_data['title']
            existing_book = AddBook.objects.filter(book_id=id, title=book_name).first()

            if not existing_book:
                new_book = AddBook(book_id=id, title=book_name)
                new_book.save()
                saved = True
            else:
                messages.warning(request, 'Book already exists with the same details.')

    if searchtitle:
        books = AddBook.objects.filter(title__icontains=searchtitle)
    else:
        books = AddBook.objects.all()

        
    
    form = BookForm()
    return render(request, 'sample.html', {'form': form, 'saved': saved, 'books': books, 'searchtitle': searchtitle})
