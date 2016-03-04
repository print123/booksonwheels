"""A Class for Book"""

from ..models import Book,Rents
from django.db.models import Count

class BookClass:
	
	def __init__(self,bookid):
		self.bookid=bookid
	def __init__(self):
		bookid=None
	
	def mark_it_unavailable(self):
		Book.Object.filter(bookid=self.bookid).update(available=False)
	
	def getSummary(self):
		return Book.object.filter(bookid=self.bookid).values('summary')
		
	def getTrending(self):		
		rentTrend = Book.objects.all().values('ISBN').annotate(total=Count('ISBN')).order_by('-total')[:3]
		res=[]
		for i in rentTrend:
			res += self.getBook(i['ISBN'])
		print res
		return res
			
	def getQuotation(self,time_dur):
		# for customer
		base_price=Book.object.filter(bookid=self.bookid).values('actual_price')
		final_price=0.1*base_price*cnt
		
		return final_price
	
	def getRent(self):
		# for uploader
		base_price=Book.object.filter(bookid=self.bookid).values('actual_price')
		final_price=0.1*base_price*cnt
		
		return final_price
	
	def getBooks(self,number):
		b=Book.objects.all()[:number]
		return b
		
	def getBook(self,ISBN):
		b=Book.objects.filter(ISBN=ISBN)[:1]
		return b
		