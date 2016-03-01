"""A Class for Book"""

from ..models import Book,Rents


class BookClass:
	
	def __init__(self,bookid):
		self.bookid=bookid
	def __init__(self):
		bookid=None
	
	def mark_it_unavailable(self):
		Book.Object.filter(bookid=self.bookid).update(available=False)
	
	def getSummary(self):
		return Book.object.filter(bookid=self.bookid).values('summary')
		
	def getTrending(self,cnt,type):
		# left to implement
		if type == 1:  # 1 for rent
			rentTrend = Rents.object.all().aggregate(Max(count(ISBN)))
			
			
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
		
		
		