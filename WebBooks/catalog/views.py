from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import Authorsform
# Create your views here.
from django.http import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book

class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 4


def some():
    pass


class BookCreate(CreateView):

    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):

    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):

    model = Book
    success_url = reverse_lazy('books')





def delete(request,id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect('/authors_add/')
    except:
        return HttpResponse('<h1>this author is not found</h1>')


def edit1(request,id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        author.firstname = request.POST.get('firstname')
        author.lastname = request.POST.get('lastname')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    else:
        return render(request, 'catalog/authors_edit1.html', context={'author': author})

def create(request):
    if request.method == 'POST':
        author = Author()
        author.firstname = request.POST.get('firstname')
        author.lastname = request.POST.get('lastname')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')




from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import secrets
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email','').strip().lower()
        username = request.POST.get('username')
        if not email:
            return render(request, 'catalog/register.html', context={'error':'fill in email'})
        if User.objects.filter(email = email).exists():
            return render(request, 'catalog/register.html', context={'error': 'there is already a person with this email'})
        if User.objects.filter(username = username).exists():
            return render(request, 'catalog/register.html', context={'error': 'there is already a person with this username'})

        user = User.objects.create_user(username=username, email=email, password=secrets.token_urlsafe(16))

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse('password_reset_confirm', kwargs={'uidb64':uid,'token':token})
        full_url = request.build_absolute_uri(reset_url)
        send_mail('set password', f'go to website to set password: {full_url}', settings.EMAIL_HOST_USER,[email])

        return render(request, 'catalog/email_sent.html', context={})
    return render(request, 'catalog/register.html', context={})

def AuthorsAdd(request):
    author = Author.objects.all()
    authorsform = Authorsform()
    return render(request, 'catalog/authors_add.html',context={'form':authorsform,'author':author})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower = self.request.user).filter(status__name__exact = 'ordered').order_by('due_back')#what is status exact

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status = '2').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'index.html', context={
        'num_books': num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instance_available,
        'num_authors':num_authors,
        'num_visits':num_visits,
        }
    )

def borrow(request,id,user):
    bookid = None
    user = User.objects.filter(id=user)
    bookinstobj = BookInstance.objects.filter(id = id)
    for book in bookinstobj:
        for use in user:
            book.borrower = use
            print(book.borrower)
        for statu in Status.objects.filter(name='ordered'):
            book.status = statu
        book.save()
        bookid = book.book.id

    return redirect('book_detail', bookid)





#other project ------------------------------------------

def task_display(request):
    tasks = Task.objects.all()

    return render(request, 'TaskManager.html', context={'tasks':tasks})

def task_add(request):
    statuses = StatusOfTask.objects.all()
    if request.method == 'POST':




        client = Task()
        client.name = request.POST.get('name')
        client.description = request.POST.get('description')
        client.due_date = request.POST.get('due_date')
        status_id=request.POST.get('status')
        status=StatusOfTask.objects.get(id=status_id)
        client.status =status
        client.save()
        return redirect('task')
    return render(request, 'TaskAdd.html',{'statuses':statuses} )

def task_edit(request,id):
    task = Task.objects.get(id=id)
    try:
        if request.method == 'POST':
            task.name = request.POST.get('name')
            task.description = request.POST.get('description')
            task.due_date = request.POST.get('due_date')
            task.status = request.POST.get('status')
            task.save()
            return HttpResponseRedirect('/taskmanager')
        else:
            return render(request, 'taskedit.html', {'task':task})
    except task.DoesNotExist:
        return HttpResponseNotFound('client not found')


def task_delete(request,id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect('/taskmanager')
    except Task.DoesNotExist:
        return HttpResponseNotFound('client not found')
