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
	
	def getCategory(self):
		catCount = Book.objects.all().values('genre').annotate(total=Count('genre'))
		print catCount
		return catCount

	def getCategoryOfRes(self,res):
		gen_counts=[]
		for r in res:
			flag=False
			for d in gen_counts:
				if d['genre'] == r.genre:
					d['total']+=1
					flag=True
					break
			if flag==False:
				gen_counts.append({'genre':r.genre,'total':1})	
		print gen_counts
		return gen_counts

  		
  		