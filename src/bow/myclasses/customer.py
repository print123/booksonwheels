"""A Class that represents a Customer """

from .cart import CartClass
from .user import UserClass
from .book import BookClass
from ..models import User, Wishlist, Book, Rents,Upload
import json
import requests
import yaml
class CustomerClass(UserClass):
    def __init__(self, userid):
        self.userid = userid

    def myBooks(self):
        """A method to display books uploaded by any  user"""
        books = Book.objects.filter(owner_id_id=self.userid)
        return books

    def currentBooks(self, userid):
        """A method to display books Rented by any  user"""
        r_books = Rents.objects.filter(userid=userid)
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

    '''
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
                Wishlist.objects.filter(userid=self.userid, ISBN=ISBN).delete()
                return True
            except:
                return False

        def getItems(self):
            """Display current items in wishlist of a user"""
            return Wishlist.object.filter(userid=self.userid)
'''
    def uploadBook(self,t_ISBN,tosell,torent,sellprice,rentprice,quantity):
        #incorrect isbn not handled only if info not found handled
        lst={}
        lst['dosell']=False
        lst['dorent']=False
        if tosell == "on":
            lst['dosell']=True
        if torent == "on":
            lst['dorent']=True
        lst['ISBN']=t_ISBN
        lst['sellprice']=sellprice
        lst['rentprice']=rentprice
        lst['quantity']=quantity
        url='https://www.googleapis.com/books/v1/volumes?q=isbn:'+(t_ISBN)
        
        lst['imageurl']=''
        lst['author']=''
        lst['title']=''
        lst['summary']=''
        lst['language']=''
        lst['publisher']=''
        lst['genre']=''
        r=requests.get(url)

        resp=r.json()
        if not 'items' in resp:
            return lst
        temp=resp['items']
        mydict=temp[0]
        print mydict
        lst['title']=mydict['volumeInfo']['title']
        

        for i in mydict['volumeInfo']['authors']:
            lst['author']=(yaml.safe_load(i))
        ISBN13=mydict['volumeInfo']['industryIdentifiers'][0]['identifier']
        ISBN10=mydict['volumeInfo']['industryIdentifiers'][1]['identifier']
        if 'imageLinks' in mydict["volumeInfo"]:
            lst['imageurl']=mydict['volumeInfo']['imageLinks']['thumbnail']
            from urllib import urlretrieve
            fname="bow\\static\\images\\"+ISBN13+".jpg"#give absolute path as where to store image
            urlretrieve(lst['imageurl'],fname)
            imageurl='images\\'+ISBN13+'.jpg'


        if 'categories' in mydict["volumeInfo"]:
            for i in mydict['volumeInfo']['categories']:
                lst['genre']=(yaml.safe_load(i))

        if 'description' in mydict["volumeInfo"]:
            lst['summary']=mydict['volumeInfo']['description']
            lst['summary']=lst['summary'][:490]
        if 'publisher' in mydict["volumeInfo"]:
            lst['publisher']=mydict['volumeInfo']['publisher']
        if 'description' in mydict["volumeInfo"]:
            lst['language']=mydict['volumeInfo']['language']
        #print lst
        return lst
       # b=Book(owner_id_id=self.userid,author=author,actual_price=price,ISBN=t_ISBN,imageurl=imageurl,genre=genre,dosell=dosell,dorent=dorent,available=True,summary=summary,publisher=publisher,language=language,title=title,rating=4.0)
        #b.save()

    def addBook(self,lst,request):
        if 'author' in lst:
            author=lst['author']
        else:
            author=request.session['author']
            del request.session['author']
        
        if 'ISBN' in lst:
            t_ISBN=lst['ISBN']
        else:
            t_ISBN=request.session['ISBN']
            del request.session['ISBN']
        dorent=request.session['dorent']
        dosell=request.session['dosell']
        sellprice=request.session['sellprice']
        rentprice=request.session['rentprice']
        quantity=request.session['quantity']
        del request.session['rentprice']
        del request.session['dorent']
        del request.session['dosell']
        del request.session['sellprice']
        del request.session['quantity']
        if 'imageurl' in lst:
            imageurl=lst['imageurl']
        else:
            imageurl1=request.session['imageurl']
            from urllib import urlretrieve
            fname="bow\\static\\images\\"+t_ISBN+".jpg"#give absolute path as where to store image
            urlretrieve(imageurl1,fname)
            imageurl='images\\'+t_ISBN+'.jpg'
            del request.session['imageurl']
        if 'summary' in lst:
            summary=lst['summary']
        else:
            summary=request.session['summary']
            del request.session['summary']
        if 'publisher' in lst:
            publisher=lst['publisher']
        else:
            publisher=request.session['publisher']
            del request.session['publisher']
        if 'language' in lst:
            language=lst['language']
        else:
            language=request.session['language']
            del request.session['language']
        if 'title' in lst:
            title=lst['title']
        else:
            title=request.session['title']
            del request.session['title']
        if 'genre' in lst:
            genre=lst['genre']
        else:
            genre=request.session['genre']
            del request.session['genre']

        b=Book(author=author,ISBN=t_ISBN,imageurl=imageurl,genre=genre,summary=summary,publisher=publisher,language=language,title=title,rating=4.0,quantity=quantity,sellquantity=quantity)
        b.save()
        nuser=Upload(owner_id_id=request.session['userid'],bookid=b,dorent=dorent,dosell=dosell,sellprice=sellprice,rentprice=rentprice,qtyuploaded=quantity,qtyavailable=quantity)
        nuser.save()