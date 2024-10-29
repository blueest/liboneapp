from django.db import models
from books.models import Book
from users.models import Profile
from django.utils import timezone

# Create your models here.
class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.user.username} borrowed {self.book.title}"
    
    
class ActivityLog(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.user.username} - {self.activity_type} on {self.timestamp}"