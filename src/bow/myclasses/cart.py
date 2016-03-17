"""A Class that represents a Customer """

from .book import BookClass
from ..models import Cart, Book, Order


class CartClass:
    def __init__(self, userid):
        self.userid = userid
        self.bookarray = Cart.objects.filter(userid=self.userid)

    def addToCart(self, ISBN, quantity):
        """A method to add a new book in Cart"""
        print self.userid
        print ISBN
        print quantity
        newCartObj = Cart(userid_id=self.userid , ISBN=ISBN , quantity=quantity)
        newCartObj.save()

    def removeFromCart(self, ISBN):
        """To remove a book from Cart"""
        Cart.objects.filter(userid=self.userid, ISBN=ISBN , quantity=quantity).delete()

    def displayCart(self):
        """To display Cart Items"""
        books = []
        for i in self.bookarray:
            b = Book.objects.get(ISBN=i.ISBN , quantity=i.quantity)
            books.append(b)
        return books

    def checkOut(self,ISBN):
        """To actually checkout"""
        bookObj = BookClass(ISBN)
        bookObj.mark_it_unavailable()
        self.removeFromCart(ISBN)