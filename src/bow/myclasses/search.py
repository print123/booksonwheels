"""Class for search Facility"""
# search on multiple attribs
from django.db.models import Q
from .book import BookClass
from ..models import Book


class SearchClass:
    def searchOnString(self, string):
        results = []
        result = Book.objects.filter(
                Q(ISBN__iexact=string) |
                Q(author__icontains=string) |
                Q(title__icontains=string) |
                Q(summary__icontains=string) |
                Q(genre__icontains=string)
        )
        b = BookClass()
        for r in result:
            res1=r.__dict__
            p=b.getPrice(r.ISBN)
            res1['sprice'] = p['sellprice']
            res1['rprice'] = p['rentprice']
            results.append(res1)
        print results
        return results
    def searchToSuggest(self, string):
        results = []
        result = Book.objects.filter(
                Q(ISBN__iexact=string) |
                Q(author__icontains=string) |
                Q(title__icontains=string) 
        )
        b = BookClass()
        for r in result:
            res1=r.__dict__
            p=b.getPrice(r.ISBN)
            res1['sprice'] = p['sellprice']
            res1['rprice'] = p['rentprice']
            results.append(res1)
        print results
        return results

    def searchOnGenre(self, genre):
        result = Book.objects.filter(genre=genre)
        return result

    def searchResOnGenre(self, genre, s):
        result = Book.objects.filter((
                                         Q(author__icontains=s) |
                                         Q(title__icontains=s) |
                                         Q(summary__icontains=s)) & Q(genre=genre))
        return result
