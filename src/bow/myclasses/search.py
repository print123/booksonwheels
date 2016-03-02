"""Class for search Facility"""
# search on multiple attribs
from django.db.models import Q
from ..models import Book


class SearchClass:

    def searchOnString(self,string):
        result=Book.objects.filter(
            Q(author__iexact=string)|
            Q(title__iexact=string)|
            Q(summary__iexact=string)|
            Q(genre__iexact=string)
            )
        return result
    ''''    
    def searchOnAuthor(self, author):
        result = Book.objects.filter(author__iexact=author)
        return result
        
    def searchOnISBN(self,ISBN):
        result = Book.objects.filter(ISBN=ISBN)
        return result

    def searchOnTitle(self,title):
        result = Book.objects.filter(title__iexact=title)
        return result

    def searchOnPublisher(self,publisher):
        result = Book.objects.filter(publisher=publisher)
        return result
    '''