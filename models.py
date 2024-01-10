from django.db import models

# Create your models here.

class AddBook(models.Model):
    book_id = models.CharField(max_length=255,primary_key=True)
    title = models.CharField(max_length=255)
