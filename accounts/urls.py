from django.urls import path
from accounts import admin, views
from accounts.views import home, BookDetail, category_search


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('categories/', views.list, name='book-list'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='single-book'),
    path('post/<int:book_id>/comment/', views.new_comment, name='new-comment'),
    path('post/<int:pk>/reload/', views.DetailedViewAfterComment.as_view(), name='book-reload'),
    path('category/<int:pk>/', category_search, name='category_search'),
    path('contact/', views.contact, name='contact'),
    path('contact/info/', views.notification, name='contact-reload'),
]