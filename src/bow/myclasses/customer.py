"""A Class that represents a Customer """

from .user import UserClass  #
# ,CartClass,BookClass,
from ..models import User, Wishlist, Book, Rents


class CustomerClass(UserClass):
    def __init__(self, userid):
        self.userid = userid

    def myBooks(self, userid):
        """A method to display books uploaded by any  user"""
        books = Book.object.filter(owner_id=userid)
        return books

    def currentBooks(self, userid):
        """A method to display books Rented by any  user"""
        r_books = Rents.object.filter(userid=userid)
        return r_books

    def buyBook(self, ISBN):
        """A method to buy any book"""

        books = Book.object.get(ISBN=ISBN, available=True)
        isAvailable = books.available
        if (isAvailable):
            # call mark it unavailablr for that bookid
            book_object = BookClass(books.bookid)
            book_object.mark_it_unAvailable()
            # add to cart
            #checkout
        return isAvailable

    class WishListClass:
        """WishList Class associated with each User"""
        def addBook(self, ISBN):
            """A method to add a new book in Wishlist"""
            try:
                w = Wishlist(userid=self.userid, ISBN=ISBN)
                w.save()
                return True
            except:
                return False

        def removeBook(self, ISBN):
            """To remove a book from wishlist"""
            try:
                Wishlist.object.filter(userid=self.userid, ISBN=ISBN).delete()
                return True
            except:
                return False

        def getItems(self):
            """Display current items in wishlist of a user"""
            return Wishlist.object.filter(userid=self.userid)
