from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class OnlineBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    availability = models.CharField(max_length=20, choices=(('physical', 'Physical'), ('online', 'Online'), ('both', 'Both')))
    file = models.FileField(upload_to='online_books/', blank=True, null=True)  # for online books
    
    def __str__(self):
        return self.title
