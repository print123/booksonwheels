"""A Class that represents a Customer """

from .book import BookClass
from ..models import Cart, Book, Order


class CartClass:
    def __init__(self, userid):
        self.userid = userid
        self.bookarray = Cart.objects.filter(userid=self.userid)

    def addToCart(self, bookid):
        """A method to add a new book in Cart"""
        print self.userid
        print bookid
        newCartObj = Cart(userid_id=self.userid , bookid=bookid)
        newCartObj.save()

    def removeFromCart(self, bookid):
        """To remove a book from Cart"""
        Cart.objects.filter(userid=self.userid, bookid=bookid).delete()

    def displayCart(self):
        """To display Cart Items"""
        books = []
        for i in self.bookarray:
            b = Book.objects.get(bookid=i.bookid)
            books.append(b)
        return books

    def checkOut(self,bookid):
        """To actually checkout"""
        bookObj = BookClass(bookid)
        bookObj.mark_it_unavailable()
        self.removeFromCart(bookid)
