"""A Class that represents a Customer """

from .book import BookClass
from ..models import Wishlist, Book, Order


class WishlistClass:
    def __init__(self, userid):
        self.userid = userid
        self.bookarray = Wishlist.objects.filter(userid_id=self.userid)

    def addToWishlist(self, ISBN):
        """A method to add a new book in Wishlist"""
        try:
            res=Wishlist.objects.get(userid_id=self.userid,ISBN=ISBN)                     
            return 0
        except:
            newWishlistObj = Wishlist(userid_id=self.userid , ISBN=ISBN)
            newWishlistObj.save()            
            i=0
            return 1

    def removeFromWishlist(self, ISBN):
        """To remove a book from Wishlist"""
        Wishlist.objects.filter(userid=self.userid, ISBN=ISBN).delete()

    def displayWishlist(self):
        """To display Wishlist Items"""
        books = []
        for i in self.bookarray:
            b = Book.objects.filter(ISBN=i.ISBN)[0]
            books.append(b)
        return books
    def getTotal(self):
        return len(self.bookarray)