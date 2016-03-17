"""A Class that represents a Customer """

from .cart import CartClass
from .user import UserClass
from .book import BookClass
from ..models import User, Wishlist, Book, Rents,Upload,Status
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
    def uploadBook(self,t_ISBN,tosell,torent,sellprice,rentprice,sellquantity,rentquantity):
        #incorrect isbn not handled only if info not found handled
        lst={}

        lst['dosell']=tosell
        lst['dorent']=torent
        lst['ISBN']=t_ISBN
        lst['sellprice']=int(sellprice)
        lst['rentprice']=int(rentprice)
        lst['sellquantity']=int(sellquantity)
        lst['rentquantity']=int(rentquantity)        

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
        if 'title' in mydict['volumeInfo']:
            lst['title']=mydict['volumeInfo']['title']
        
        if 'authors' in mydict['volumeInfo']:
            for i in mydict['volumeInfo']['authors']:
                lst['author']=(yaml.safe_load(i))
        ISBN13=mydict['volumeInfo']['industryIdentifiers'][0]['identifier']
        ISBN10=mydict['volumeInfo']['industryIdentifiers'][1]['identifier']
        lst['ISBN']=ISBN13
        

        #summary=mydict['volumeInfo']['description']

        

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
            lst['summary']=lst['summary'][:990]
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
        #print dorent        
        dosell=request.session['dosell']
        #print dosell
        sellprice=int(request.session['sellprice'])
        #print sellprice
        rentprice=int(request.session['rentprice'])
        #print rentprice
        sellquantity=int(request.session['sellquantity'])
        #print sellquantity
        rentquantity=int(request.session['rentquantity'])
        #print rentquantity
        del request.session['rentprice']
        del request.session['dorent']
        del request.session['dosell']
        del request.session['sellprice']
        del request.session['sellquantity']
        del request.session['rentquantity']
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
        self.updatetables(request.session['userid'],t_ISBN,dosell,dorent,int(sellquantity),int(rentquantity),author,imageurl,genre,summary,publisher,language,title,4.0,sellprice,rentprice) 

    def updatetables(self,owner,ISBN,dosell,dorent,sellquantity,rentquantity,author,imageurl,genre,summary,publisher,language,title,rating,sellprice,rentprice):
        bookObj=Book.objects.filter(ISBN=ISBN).first()
        if bookObj is not None:
            if dosell:       
                bookObj.quantity=bookObj.quantity+sellquantity         
                bookObj.sellquantity=bookObj.sellquantity+sellquantity
            if dorent:
                bookObj.quantity=bookObj.quantity+rentquantity
            bookObj.save()
        else:
            qty=sellquantity+rentquantity
            qtys=sellquantity
            b=Book(author=author,ISBN=ISBN,imageurl=imageurl,genre=genre,summary=summary,publisher=publisher,language=language,title=title,rating=4.0,quantity=qty,sellquantity=qtys)        
            b.save()
        b1=BookClass()
        bookid=b1.getBookid(ISBN)        
        b1.add_seller(bookid,dosell,dorent,sellprice,rentprice,int(int(sellquantity)+int(rentquantity)),owner)

        if dosell and dorent:
            statObj=Status.objects.filter(ISBN=ISBN,sellprice=sellprice,rentprice=rentprice).first()
            if statObj is not None:
                statObj.sellquantity=statObj.sellquantity+sellquantity
                statObj.quantity=statObj.quantity+sellquantity+rentquantity
                statObj.save()
            else:                
                st=Status(ISBN=ISBN,sellprice=sellprice,sellquantity=sellquantity,rentprice=rentprice,quantity=int(int(sellquantity)+int(rentquantity)))
                st.save()
        elif dosell:
            statObj=Status.objects.filter(ISBN=ISBN,sellprice=sellprice).first()
            if statObj is not None:
                statObj.sellquantity=statObj.sellquantity+sellquantity
                statObj.quantity=statObj.quantity+sellquantity
                statObj.save()
            else:
                st=Status(ISBN=t_ISBN,sellprice=sellprice,sellquantity=sellquantity,rentprice=0,quantity=sellquantity)
                st.save()
        elif dorent:
            statObj=Status.objects.filter(ISBN=ISBN,rentprice=rentprice).first()
            if statObj is not None:                
                statObj.quantity=statObj.quantity+rentquantity
                statObj.save()
            else:
                st=Status(ISBN=ISBN,sellprice=0,sellquantity=0,rentprice=rentprice,quantity=rentquantity)
                st.save()