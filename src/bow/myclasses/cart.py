"""A Class that represents a Customer """

from .book import BookClass
from ..models import Cart, Book, Order


class CartClass:
    def __init__(self, userid):
        self.userid = userid
        self.bookarray = Cart.objects.filter(userid_id=self.userid)

    def addToCart(self, ISBN,quantity,dosell):
        """A method to add a new book in Cart"""
        print ISBN
        print self.userid
        newCartObj = Cart(userid_id=self.userid , ISBN=ISBN,quantity=quantity,dosell=dosell,sellprice=100)
        newCartObj.save()

    def removeFromCart(self, ISBN):
        """To remove a book from Cart"""
        Cart.objects.filter(userid=self.userid, ISBN=ISBN).delete()
        #Come here after a while  

    def displayCart(self):
        """To display Cart Items"""
        books = []
        quant=[]
        for i in self.bookarray:
            print "onn"
            b = Book.objects.filter(ISBN=i.ISBN)[0]
            #q = Cart.object.filter(ISBN=i.ISBN).values('qunatity')
            print i.sellprice
            #print "k"
            q=i.quantity
            boo=b.__dict__
            boo['quantity']=i.quantity
            boo['sellprice']=i.sellprice
            books.append(boo)
            #quant.append(q)

        return books

    def checkOut(self,ISBN):
        """To actually checkout"""
        bookObj = BookClass(ISBN)
        bookObj.mark_it_unavailable()
        self.removeFromCart(ISBN)