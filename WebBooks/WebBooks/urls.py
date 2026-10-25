"""
URL configuration for WebBooks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Imprt the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('accounts/', include('django.contrib.auth.urls')),

    #other projects ------------------------
    path('taskmanager', views.task_display, name = 'task'),
    path('taskmanageradd/', views.task_add, name = 'taskadd'),
    path('taskmanageredit/<int:id>', views.task_edit, name = 'taskedit'),
    path('taskmanagerdelete/<int:id>', views.task_delete, name = 'taskdelete'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book_detail'),

    url(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    path('authors_add/', views.AuthorsAdd, name = 'authors_add'),
    path('edit1/<int:id>', views.edit1, name = 'edit1'),
    path('delete/<int:id>', views.delete, name = 'delete'),
    path('create/', views.create, name = 'create'),
    path('register/', views.register, name = 'register'),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'^borrow/<int:id>/<int:user>', views.borrow, name='borrow'),
    url(r'book/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'book/update/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_update'),
    url(r'book/delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name='book_delete'),

]


