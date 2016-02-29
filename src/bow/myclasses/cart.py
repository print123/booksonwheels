"""A Class that represents a Customer """


from .book import BookClass
from ..models import Cart,Book,Order

class CartClass:
		
	def __init__(self,userid):
		self.userid=userid		
		bookarray=Cart.object.filter(userid=userid)
		
		
	def addToCart(self,bookid,userid):
		"""A method to add a new book in Cart"""
		newCartObj=Cart()
		newCartObj.Save()
		
	def removeFromCart(self,bookid,userid):
		"""To remove a book from Cart"""
		Cart.object.filter(userid=self.userid, bookid=bookid).delete()
	
	
	def displayCart(self,userid):
		"""To display Cart Items"""
		return Cart.object.filter(userid=self.userid)		
		
	def checkOut(self,userid,bookid):
		"""To actually checkout"""
		bookObj=BookClass(bookid)
		bookObj.mark_it_unavailable()
		self.removeFromCart(bookid,userid)		