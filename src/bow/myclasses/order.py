"""Class represnting Order """

from .book import BookClass
from ..models import Order, Payment, Book, Rents

class OrderClass:
	def __init__(self, userid):
		bookid = None
		self.userid = userid
		self.orderarray = Order.objects.filter(userid_id=self.userid)		
		self.rentarray = Rents.objects.filter(userid_id=self.userid)
		
		"""status ="""
	def updateStatus(self,orderid):
		t_order=Order.objects.filter(orderid=orderid)
	def displayOrders(self):		
		books=[]
		quant=[]			
		for i in self.orderarray:     			
			b = Book.objects.get(bookid=i.bookid_id)
			p = Payment.objects.get(paymentid=i.paymentid_id)

			#q = Cart.object.filter(ISBN=i.ISBN).values('qunatity')            			
			q=i.quantity

			boo=b.__dict__
			boo['quantity']=i.quantity			
			boo['sellprice']=p.amount
			boo['type']="Buy"
			#boo['timeperiod']=i.timeperiod
			#boo['dosell']=i.dosell			
			books.append(boo)

		for j in self.rentarray:					
			b1 = Book.objects.get(bookid=j.bookid_id)
			r1 = Payment.objects.get(paymentid=j.paymentid_id)

			q=j.quantity
			boo1=b1.__dict__
			boo1['quantity']=j.quantity
			boo1['sellprice']=r1.amount
			boo1['type']="Rent"
			#boo['timeperiod]=i.timeperiod
			#boo['dosell']=i.dosell			
			books.append(boo1)				
		return books