from builtins import bool
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render,  get_object_or_404
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, FormView
import requests
from accounts.models import Book, Comment, Category, Feedback

def home(request):
    featured = Book.objects.filter(featured=True)
    latest = Book.objects.filter(latest=True)


    context = {
        'featured': featured,
        'latest': latest
    }
    return render(request, 'index.html', context)


class BookDetail(DetailView):
    template_name = 'single-product.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().distinct()
        context['most_recent'] = Book.objects.filter(latest=True)
        context['queryset'] = Book.objects.all()

        # url = 'https://www.goodreads.com/book/review_counts.json'
        # params = {'isbns': '045146155X', 'api-key':'3zqJ6KvRwsmSazprXEgw&fbclid=IwAR1IKB7xB9PlrSWvuwjlC25DUIrMPKsJZWThM5MMVLqON-ZAzSzlzjtyWzc'}
        # response = requests.get(url, params=params)

        response = requests.get(
            'https://www.goodreads.com/book/review_counts.json?isbns=045146155X&'
            'api-key=3zqJ6KvRwsmSazprXEgw&fbclid=IwAR1IKB7xB9PlrSWvuwjlC25DUIrMPKsJZWThM5MMVLqON-ZAzSzlzjtyWzc')
        review = response.json()

        context['reviews_count']= review['books'][0]['reviews_count']
        context['ratings_count']= review['books'][0]['ratings_count']
        context['text_reviews_count']= review['books'][0]['text_reviews_count']
        context['work_ratings_count']= review['books'][0]['work_ratings_count']
        context['average_rating']= review['books'][0]['average_rating']




        return context




def new_comment(request, book_id):
        post = get_object_or_404(Book, id=book_id)

        try:
            username = request.POST['username']
            email = request.POST['useremail']
            comment = request.POST['usercomment']
        except KeyError as key_err:
            return handle_error(request, post, str(key_err))

        if comment != "" and email != "" and username != "":
            post.comment_set.create(comment=comment, user_name=username, email=email)


            return HttpResponseRedirect(reverse('book-reload', args=(book_id,)))
        else:
            return handle_error(request, post, "ERROR: All fields are required!")

def handle_error(request, book, err_msg):
    return render(request, 'single-product.html', {
        'book': book,
        'error_msg': err_msg
    })

class DetailedViewAfterComment(DetailView):
    template_name = 'single-product.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().distinct()
        context['most_recent'] = Book.objects.filter(latest=True)
        return context

def list(request):
    categories = Category.objects.all().distinct()
    most_recent = Book.objects.filter(latest=True)
    book_list = Book.objects.all()

    paginator = Paginator(book_list, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'categories': categories,
    }
    return render(request, 'category.html', context)

def search(request):
    categories = Category.objects.all().distinct()
    most_recent = Book.objects.filter(latest=True)

    queryset = Book.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(long_description__icontains=query)
        ).distinct()

    num_of_posts = queryset.count()

    if num_of_posts == 0:
        result_message = "No results for your search"
    else:
        result_message = "Search results: "

    context = {
        'queryset': queryset,
        'most_recent': most_recent,
        'categories': categories,
        'result_message': result_message,
        'num_posts': num_of_posts
    }
    return render(request, 'category_search_results.html', context)

def category_search(request, pk):
    category = get_object_or_404(Category, id=pk)
    print(category.title)
    queryset = Book.objects.filter(categories__title__icontains=category.title)

    categories = Category.objects.all().distinct()
    most_recent = Book.objects.filter(latest=True)

    num_of_posts = queryset.count()

    if num_of_posts == 0:
        result_message = "No results for your search"
    else:
        result_message = "Search results (Category " + category.title + "):"

    context = {
        'queryset': queryset,
        'most_recent': most_recent,
        'categories': categories,
        'result_message': result_message,
        'num_posts': num_of_posts
    }

    return render(request, 'category_search_results.html', context)

def handle_error_contact(request, feedback, err_msg):
    return render(request, 'contact.html', {
        'feedback': feedback,
        'error_msg': err_msg,
        'success': False
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        description = request.POST['description']
        feedback = Feedback()

        if name != "" and email != "" and subject != "" and description != "":
            feedback.name = name
            feedback.email = email
            feedback.subject = subject
            feedback.description = description
            feedback.save()

            return HttpResponseRedirect(reverse('contact-reload'))
        else:
            return handle_error_contact(request, feedback, "ERROR: All fields are required!")

    context = {
        'success': True,
    }
    return render(request, 'contact.html', context)


def notification(request):
    return render(request, 'after_new_feedback.html')