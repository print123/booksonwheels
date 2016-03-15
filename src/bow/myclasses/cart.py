"""A Class that represents a Customer """

from .book import BookClass
from ..models import Cart, Book, Order


class CartClass:
    def __init__(self, userid):
        self.userid = userid
        self.bookarray = Cart.objects.filter(userid_id=self.userid)

    def addToCart(self,ISBN,quantity):
        """A method to add a new book in Cart"""        
        newCartObj = Cart(userid_id=self.userid , ISBN=ISBN,quantity=quantity)
        newCartObj.save()

    def removeFromCart(self, ISBN):
        """To remove a book from Cart"""
        newCartObj=Cart.objects.get(userid=self.userid, ISBN=ISBN)
        #Come here after a while        

    def displayCart(self):
        """To display Cart Items"""
        books = []
        for i in self.bookarray:
            b = Book.objects.get(ISBN=i.ISBN)
            books.append(b)
        return books

    def checkOut(self,bookid):
        """To actually checkout"""
        bookObj = BookClass(bookid)
        bookObj.mark_it_unavailable()
        self.removeFromCart(bookid)
