

"""A Class that represents a Customer """
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .cart import CartClass
from .user import UserClass
from .book import BookClass
from .admin import AdminClass
from ..models import User, Payment,Wishlist, Book, Rents,Upload,Status,Cart,Order
import json
import requests
import yaml
class CustomerClass(UserClass):
    def __init__(self, userid):
        self.userid = userid

    def myBooks(self):
        """A method to display books uploaded by any  user"""
        boo = Upload.objects.filter(owner_id_id=self.userid)
        books=[]
        for b in boo:
            t=Book.objects.get(bookid=b.bookid_id)
            p={}
            p=t.__dict__
            p['actual_price']=float(b.sellprice)
            p['rentprice']=float(b.rentprice)            
            p['dosell']=b.dosell
            p['dorent']=b.dorent
            p['qty']=b.qtyuploaded
            p['aqty']=b.qtyavailable                    
            books.append(p)
        return books
    def getCategoryOf(self, res):
        gen_counts = []
        #t = 0
        for r in res:
            flag = False
            if r['dosell']:
                q="Sell"
            else:
                q="Rent"
            for d in gen_counts:
                if d['genre'] == q:
                    d['total'] += 1
                    #t += 1
                    flag = True
                    break
            if flag == False:
                #t += 1
                gen_counts.append({'genre': q, 'total': 1})
        return gen_counts


    def showCategory(self, s):
        boo = Upload.objects.filter(owner_id_id=self.userid, dosell=s)
        books=[]
        for b in boo:
            t=Book.objects.get(bookid=b.bookid_id)
            p={}
            p=t.__dict__
            p['actual_price']=b.sellprice
            p['rentprice']=b.rentprice
            p['dosell']=b.dosell
            p['dorent']=b.dorent
            p['qty']=b.qtyavailable
            books.append(p)
        return books

    def currentBooks(self, userid):
        """A method to display books Rented by any  user"""
        r_books = Rents.objects.filter(userid=userid)
        return r_books

    def addDeliveryDetails(self,contactno,address):
        """A method to add deivery details of the order in database for a customer"""
        custObj=User.objects.filter(userid=self.userid).first()        
        custObj.contact_no=contactno        
        custObj.address=address        
        custObj.save()
        

    def bookCheckout(self):                
        """A method that implements checkout logic"""
        cartObj=Cart.objects.filter(userid_id=self.userid)                            
        for i in cartObj:            
            if i.dosell:                
                bookObj=BookClass()                
                temp_id=bookObj.getBookid(i.ISBN)
                bObj=Book.objects.filter(ISBN=i.ISBN).first()            
                statObj=Status.objects.filter(ISBN=i.ISBN,sellprice=i.sellprice).first()                                                                       
                squant=statObj.sellquantity                
                i.quantity=min(squant,i.quantity)                
                bObj.quantity=bObj.quantity-i.quantity                
                bObj.sellquantity=bObj.sellquantity-i.quantity                
                bObj.save()                
                while (i.quantity>0):
                    temp=i.quantity
                    oid,i.quantity=bookObj.getOwner(temp_id,i.quantity,i.dosell,i.sellprice)                          
                    price=i.sellprice*(temp-i.quantity)
                    statObj.sellquantity=statObj.sellquantity-(temp-i.quantity)
                    statObj.quantity=statObj.quantity-(temp-i.quantity)                   
                    payment=Payment(mode='cd',amount=price,ispending=True)
                    payment.save()
                    order=Order(userid_id=self.userid,paymentid_id=payment.paymentid,bookid_id=temp_id,owner_id_id=oid,quantity=(temp-i.quantity))
                    order.save()
                    a=AdminClass()
                    a.mailowner(oid,temp_id,"buy",(temp-i.quantity))
                statObj.save()
            else:
                try:
                    bookObj=BookClass()                
                    temp_id=bookObj.getBookid(i.ISBN)                                    
                    bObj=Book.objects.filter(ISBN=i.ISBN).first()                
                    statObj=Status.objects.filter(ISBN=i.ISBN,rentprice=i.sellprice).first()                                                                      
                    squant=statObj.quantity
                    i.quantity=min(squant,i.quantity)                
                    bObj.quantity=bObj.quantity-i.quantity                
                    bObj.save()
                    while(i.quantity>0):                    
                        temp=i.quantity                                        
                        oid,i.quantity=bookObj.getOwner(temp_id,i.quantity,i.dosell,i.sellprice)                                        
                        price=i.sellprice*(temp-i.quantity)                                        
                        statObj.quantity=statObj.quantity-(temp-i.quantity)                    
                        payment=Payment(mode='cd',amount=price,ispending=True)                                        
                        payment.save()                          
                        date_of_return = (datetime.today()+relativedelta(months=int(i.timeperiod))).isoformat()                                                            
                        rent=Rents(ISBN=i.ISBN,userid_id=self.userid,paymentid_id=payment.paymentid,bookid_id=temp_id,owner_id_id=oid,quantity=temp-i.quantity,date_of_return=date_of_return)                                                            
                        rent.save()
                        a=AdminClass()
                        a.mailowner(oid,temp_id,"rent",temp-i.quantity)                                        
                except Exception as ex:
                    print "hey bro"
                    print ex
            i.delete()
            


    def removeBook(self,bookid,sellprice,rentprice):#future arguments dosell,dorent and prices        
        """A method to remove a book from database for user"""
        upObj=Upload.objects.filter(owner_id_id=self.userid,bookid_id=bookid,sellprice=sellprice,rentprice=rentprice).first()
        sqty=upObj.sqtyavailable
        qty=upObj.qtyavailable                        
        upObj.delete()        
        bookObj=Book.objects.filter(bookid=bookid).first()                
        t_ISBN=bookObj.ISBN        
        if(bookObj.quantity == qty):            
            bookObj.delete()
        else:            
            bookObj.quantity=bookObj.quantity-qty            
            bookObj.sellquantity=bookObj.sellquantity-sqty
            bookObj.save()                
        if sellprice==999999.00:
            sellprice=0
        if rentprice==999999.00:
            rentprice=0
        statObj=Status.objects.filter(ISBN=t_ISBN,sellprice=sellprice,rentprice=rentprice).first()        
        if(statObj.quantity == qty):            
            statObj.delete()
        else:            
            statObj.quantity=statObj.quantity-qty            
            statObj.sellquantity=statObj.sellquantity-sqty
            statObj.save()
    
    def updateQuantity(self,bookid,ISBN,sellprice,rentprice,sellquant,rentquant):
        """A method that allows user to update quantity of the book"""
        try:            
            import decimal
            print rentquant
            upObj=Upload.objects.filter(owner_id_id=self.userid,bookid_id=bookid,sellprice=sellprice,rentprice=rentprice).first()            
            if sellquant == 0:
                sellquant=upObj.sqtyuploaded            
            if rentquant == 0:
                rentquant = (upObj.qtyuploaded-upObj.sqtyuploaded)
            newQty=decimal.Decimal(sellquant+rentquant)            
            oldQty=upObj.qtyuploaded
            oldaQty=upObj.qtyavailable            
            diff=newQty-oldQty                    
            diff1=sellquant-upObj.sqtyuploaded
            upObj.qtyuploaded=upObj.qtyuploaded+diff            
            upObj.sqtyuploaded=sellquant
            upObj.qtyavailable=upObj.qtyavailable+diff            
            upObj.sqtyavailable=upObj.sqtyavailable+diff1
            upObj.save()
            bookObj=Book.objects.filter(bookid=bookid).first()
            bookObj.quantity=bookObj.quantity+diff
            bookObj.sellquantity=bookObj.sellquantity+diff1
            t_ISBN=bookObj.ISBN
            bookObj.save()
            statObj=Status.objects.filter(ISBN=t_ISBN,rentprice=rentprice,sellprice=sellprice).first()            
            statObj.quantity=statObj.quantity+diff
            statObj.sellquantity=statObj.sellquantity+diff1
            statObj.save()
        except Exception as ex:
            print ex
    

    def uploadBook(self,t_ISBN,got):
        """A method to upload a book"""
        #incorrect isbn not handled only if info not found handled
        lst={}        
        lst['ISBN']=t_ISBN                
        got['ISBN']=t_ISBN
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
            got['title']=lst['title']
        
        if 'authors' in mydict['volumeInfo']:
            for i in mydict['volumeInfo']['authors']:
                lst['author']=(yaml.safe_load(i))
                got['author']=lst['author']
        ISBN13=mydict['volumeInfo']['industryIdentifiers'][0]['identifier']
        ISBN10=mydict['volumeInfo']['industryIdentifiers'][1]['identifier']
        #lst['ISBN']=t_ISBN        

        #summary=mydict['volumeInfo']['description']

        

        if 'imageLinks' in mydict["volumeInfo"]:
            lst['imageurl']=mydict['volumeInfo']['imageLinks']['thumbnail']
            from urllib import urlretrieve
            fname="bow\\static\\images\\"+ISBN13+".jpg"#give absolute path as where to store image
            urlretrieve(lst['imageurl'],fname)
            got['imageurl']="/static/images/"+ISBN13+".jpg"
            imageurl='images\\'+ISBN13+'.jpg'


        if 'categories' in mydict["volumeInfo"]:
            for i in mydict['volumeInfo']['categories']:
                lst['genre']=(yaml.safe_load(i))
                got['genre']=lst['genre']

        if 'description' in mydict["volumeInfo"]:
            lst['summary']=mydict['volumeInfo']['description']
            lst['summary']=lst['summary'][:990]
            got['summary']=lst['summary']
        if 'publisher' in mydict["volumeInfo"]:
            lst['publisher']=mydict['volumeInfo']['publisher']
            got['publisher']=lst['publisher']
        if 'description' in mydict["volumeInfo"]:
            lst['language']=mydict['volumeInfo']['language']
            got['language']=lst['language']
        #print lst
        return lst        
       # b=Book(owner_id_id=self.userid,author=author,actual_price=price,ISBN=t_ISBN,imageurl=imageurl,genre=genre,dosell=dosell,dorent=dorent,available=True,summary=summary,publisher=publisher,language=language,title=title,rating=4.0)
        #b.save()

    def addBook(self,lst,request):  
        for i in lst:
            print i     
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
        dorent=False
        dosell=False
        if 'rent' in lst:
            if lst['rent']=="on":
                dorent=True
        #print dorent      
        if 'sell' in lst:  
            if lst['sell']=="on":
                dosell=True
        #print dosell
        sellprice=999999 
        rentprice=999999
        sellquantity=0
        rentquantity=0
        if not lst['sellprice']=='':
            sellprice=int(lst['sellprice'])
            sellquantity=int(lst['sellquantity'])
        #print sellprice
        if not lst['rentprice']=='':
            rentprice=int(lst['rentprice'])
            rentquantity=int(lst['rentquantity'])
        #print rentprice
        

        #print sellquantity
        
        #print rentquantity        
        imageurl=""
        if 'imageurl' in lst:
            imageurl=lst['imageurl']            
        elif 'old' in request.session:
            imageurl=request.session['imageurl']
            imageurl1=request.session['imageurl']                     
            from urllib import urlretrieve
            fname="bow\\static\\images\\"+t_ISBN+".jpg"#give absolute path as where to store image
            #urlretrieve(imageurl1,fname)
            imageurl='images\\'+t_ISBN+'.jpg'
            del request.session['imageurl']
        else:
            imageurl1=request.session['imageurl']            
            from urllib import urlretrieve
            fname="bow\\static\\images\\"+t_ISBN+".jpg"#give absolute path as where to store image
            urlretrieve(imageurl1,fname)
            imageurl='images\\'+t_ISBN+'.jpg'
            del request.session['imageurl']
        
        from PIL import Image
        import PIL
        
        furl="bow/static/"+imageurl              
        img=Image.open(furl)
        img=img.resize((128,192),PIL.Image.ANTIALIAS)
        img.save(furl)
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
        b1.add_seller(bookid,dosell,dorent,sellprice,rentprice,int(sellquantity),int(int(sellquantity)+int(rentquantity)),owner)

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
                st=Status(ISBN=ISBN,sellprice=sellprice,sellquantity=sellquantity,rentprice=0,quantity=sellquantity)
                st.save()
        elif dorent:
            statObj=Status.objects.filter(ISBN=ISBN,rentprice=rentprice).first()
            if statObj is not None:                
                statObj.quantity=statObj.quantity+rentquantity
                statObj.save()
            else:
                st=Status(ISBN=ISBN,sellprice=0,sellquantity=0,rentprice=rentprice,quantity=rentquantity)
                st.save()
