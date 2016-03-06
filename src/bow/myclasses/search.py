"""Class for search Facility"""
# search on multiple attribs
from django.db.models import Q
from ..models import Book


class SearchClass:

    def searchOnString(self,string):
        result=Book.objects.filter(
            Q(author__icontains=string)|
            Q(title__icontains=string)|
            Q(summary__icontains=string)|
            Q(genre__icontains=string)
            )
        return result

    def searchOnGenre(self,genre):
    	result=Book.objects.filter(genre=genre)
    	return result
    	
