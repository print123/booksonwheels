"""Class represnting Order """

from .book import BookClass
from ..models import Order, Payment, Book

class OrderClass:
	def __init__(self, userid):
		bookid = None
		self.userid = userid
		self.orderarray = Order.objects.filter(userid_id=self.userid)
		"""status ="""
	def updateStatus(self,orderid):
		t_order=Order.objects.filter(orderid=orderid)
	def displayOrders(self):
		books = []
		quant=[]			
		for i in self.orderarray:            			
			b = Book.objects.filter(bookid=i.bookid_id)			
			#q = Cart.object.filter(ISBN=i.ISBN).values('qunatity')            			
			q=i.quantity
			boo=b.__dict__
			boo['quantity']=i.quantity
			#boo['sellprice']=i.sellprice
			#boo['timeperiod']=i.timeperiod
			#boo['dosell']=i.dosell			
			books.append(boo)
			#quant.append(q)			
		

		return books