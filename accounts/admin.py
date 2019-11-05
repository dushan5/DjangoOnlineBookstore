from django.contrib import admin

from .models import  Category, Book, Comment, Feedback


admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Feedback)