from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=20,help_text='genre of book', verbose_name=' genre')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20,help_text='the language your book is written in', verbose_name=' language')

    def __str__(self):
        return self.name

class Author(models.Model):
    firstname = models.CharField(max_length=20,help_text='write the authors first name', verbose_name='first name')
    lastname = models.CharField(max_length=20, help_text='write the authors last name', verbose_name='last name')
    date_of_birth = models.DateField(help_text='write the authors date of birth', verbose_name='date of birth', null = True, blank=True)
    date_of_death = models.DateField(help_text='write the authors date of death', verbose_name='date of death',  null = True, blank=True)
    def __str__(self):
        return self.lastname


class Book(models.Model):
    title = models.CharField(max_length=20, help_text='write the title of the book', verbose_name='title')
    genre = models.ForeignKey('Genre',on_delete=models.CASCADE, help_text='choose book genre', verbose_name='genre', null = True)
    language = models.ForeignKey('Language',on_delete=models.CASCADE, help_text='choose the language of your book', verbose_name='language', null = True)
    author = models.ManyToManyField('Author', help_text='choose book author', verbose_name='author')
    summary = models.CharField(max_length=500, help_text='write the short summary of the book', verbose_name='summary')
    isbn = models.CharField(max_length=13, help_text='has to contain 13 symbols(book id)', verbose_name='isbn')

    def __str__(self):
        return self.title
    def display_authors(self):
        return '. '.join([author.lastname for author in self.author.all()])
    display_authors.short_description = 'Authors'
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


class Status(models.Model):
    name = models.CharField(max_length=20, help_text='enter status of the book exemple', verbose_name='status of example')
    def __str__(self):
        return self.name

class BookInstance(models.Model):
    book = models.ForeignKey('Book',on_delete=models.CASCADE,null = True)
    in_nom = models.CharField(max_length=100, help_text='enter inventory number of book',
                            verbose_name='invintory number')
    imprint = models.CharField(max_length=20, help_text='enter date of publication and publish house',
                            verbose_name='publish house')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True, help_text='change status of example',
                            verbose_name='status')
    due_back = models.DateField(help_text='enter when status expires', verbose_name='date of status end',
                                     null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 help_text='choose borrower of book',
                                 verbose_name='borrower')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '%s %s %s' % (self.in_nom, self.book, self.status )


#OOOOOOOOOOOOOOTTTTTHHHHEEEERRRRR PRRRROOOOJJJJEEECCTTSS  _---------------------------------------------------------

class Blog(models.Model):
    title = models.CharField(max_length=20, help_text='enter blog title ', verbose_name='title')
    content = models.TextField(max_length=300, help_text='enter the content/description of the blog ', verbose_name='content')
    created_at = models.DateTimeField(help_text='when was the blog is created', verbose_name='created at', auto_now_add=True)
    updated_at = models.DateTimeField(help_text='when was the blog is updated', verbose_name='updated at',
                                      auto_now=True)
    is_published = models.BooleanField(default='true',help_text='is it publishe or not', verbose_name='published?')
    def __str__(self):
        return self.title

#-------------------------------------------------


class StatusOfTask(models.Model):
    name = models.CharField(max_length=20, help_text='enter status of the status exemple', verbose_name='status')
    def __str__(self):
        return self.name
class Task(models.Model):
    name = models.CharField(max_length=20, help_text='enter name of the task ', verbose_name='name')
    description = models.TextField(max_length=300, help_text='description of the task', verbose_name='description')
    due_date = models.DateField(help_text='the due date of when your task MUST be completed', verbose_name='due date')
    status = models.ForeignKey('StatusOfTask', on_delete=models.CASCADE, null=True, help_text='change status of task',
                               verbose_name='status')

    def __str__(self):
        return self.name

