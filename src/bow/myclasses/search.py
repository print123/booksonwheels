"""Class for search Facility"""
# search on multiple attribs
from ..models import Book


class SearchClass:

    def searchOnAuthor(self, author):
        result = Book.objects.filter(author=author)
        return result

    def searchOnISBN(self,ISBN):
        result = Book.objects.filter(ISBN=ISBN)
        return result

    def searchOnTitle(self,title):
        result = Book.objects.filter(title=title)
        return result

    def searchOnPublisher(self,publisher):
        result = Book.objects.filter(publisher=publisher)
        return result

