from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse




class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[str(self.id)])


class Book(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    short_description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField()
    featured = models.BooleanField()
    latest = models.BooleanField(default= False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single-book', args=[str(self.id)])

    def format_date(self):
        return self.timestamp.strftime('%b %d, %Y')


class Comment(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=25, null=False, blank=False)
    comment = models.CharField(max_length=500, null=False, blank=False)
    email = models.CharField(max_length=500, null=False, blank=False)
    for_book = models.ForeignKey(to=Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " : " + self.subject