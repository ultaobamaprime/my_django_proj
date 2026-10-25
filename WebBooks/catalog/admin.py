from django.contrib import admin
from .models import *
# Register your models here.

#admin.site.register(Author)
admin.site.register(Language)
#admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Status)
#admin.site.register(BookInstance)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('lastname','firstname')
    fields = ['firstname','lastname',
              ('date_of_birth','date_of_death')]
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInLine(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','language','genre','display_authors')
    list_filter = ('genre','author')
    inlines = [BooksInstanceInLine]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status', 'borrower', 'due_back','id')
    list_filter = ('book','status')
    fieldsets = [
        ('Book',{
            'fields': ('book','imprint','in_nom')

        }),
        ('Status', {
            'fields': ('status', 'due_back','borrower')

        })

    ]


@admin.register(Blog)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','content','created_at','updated_at','is_published')
    list_filter = ('is_published','created_at')


#OOOOOOOOTTTTTTTHHHHHHHHHHHHHHHHEEEEEEEEEEEERRRRRRRRRRR

admin.site.register(Task)
admin.site.register(StatusOfTask)
