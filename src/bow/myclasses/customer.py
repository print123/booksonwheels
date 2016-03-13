"""A Class that represents a Customer """

from .cart import CartClass
from .user import UserClass
from .book import BookClass
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
            cartObj=CartClass(userid,books.bookid)
            cartObj.addToCart(books.bookid,userid)			
            cartObj.checkOut(userid,books.bookid)
        return isAvailable
    def rentBook(self,ISBN):
        book_to_rent=Book.object.get(ISBN=ISBN,available=True)
        bookObj=Book(book_to_rent.bookid)
        timdur=1#to be discussed yet
        temp_var=bookObj.getQuotation(timedur)
        #ask for confirmation from user
        cartObj=CartClass(userid,book_to_rent.bookid)
        cartObj.addToCart(book_to_rent.bookid,userid)
        cartObj.checkOut(userid,book_to_rent.bookid)


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

    def uploadBook(self,t_ISBN):
        r=requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:%s'+t_ISBN)
        resp=r.json()
        temp=resp['items']
        mydict=temp[0]

        title=mydict['volumeInfo']['title']

        author=mydict['volumeInfo']['authors']

        ISBN10=mydict['volumeInfo']['industryIdentifiers'][0]['identifier']
        ISBN13=mydict['volumeInfo']['industryIdentifiers'][1]['identifier']

        imageurl=mydict['volumeInfo']['imageLinks']['thumbnail']    

        genre=mydict['volumeInfo']['categories']

        summary=mydict['volumeInfo']['description']

        publisher=mydict['volumeInfo']['publisher']

        language=mydict['volumeInfo']['language']

        b=Book.object.filter(owner_id=self.userid,ISBN=t_ISBN,actual_price=actual_price,genre=genre,summary=summary)
        b.save(available=True)