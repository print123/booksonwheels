
"""A Class that represents a Customer """

from .book import BookClass
from ..models import Cart, Book, Order,Status


class CartClass:
    def __init__(self, userid):
        self.userid = userid
        self.bookarray = Cart.objects.filter(userid_id=self.userid)

    def addToCart(self, ISBN,quantity,dosell,price,timeperiod):
        """A method to add a new book in Cart"""                
        try:            
            res=Cart.objects.get(userid_id=self.userid,ISBN=ISBN,dosell=dosell,sellprice=price,timeperiod=timeperiod)            
            res.quantity=int(res.quantity)+int(quantity)
            res.save()            
        except:            
            newCartObj = Cart(userid_id=self.userid , ISBN=ISBN,quantity=quantity,dosell=dosell,sellprice=price,timeperiod=timeperiod)            
            newCartObj.save()            

    def removeFromCart(self, ISBN, sellprice):
        """To remove a book from Cart"""

        Cart.objects.filter(userid=self.userid, ISBN=ISBN, sellprice=sellprice).delete()
 

    def displayCart(self):
        """To display Cart Items"""
        books = []
        quant=[]
        for i in self.bookarray:            
            b = Book.objects.filter(ISBN=i.ISBN)[0]
            #q = Cart.object.filter(ISBN=i.ISBN).values('qunatity')            
            #print "k"
            q=i.quantity
            boo=b.__dict__
            boo['quantity']=i.quantity
            boo['sellprice']=i.sellprice
            boo['timeperiod']=i.timeperiod
            boo['dosell']=i.dosell
            books.append(boo)
            #quant.append(q)

        return books

    def checkOut(self,ISBN):
        """To actually checkout"""
        bookObj = BookClass(ISBN)
        bookObj.mark_it_unavailable()
        self.removeFromCart(ISBN)
    
    def getTotal(self):
        return len(self.bookarray)


    def update(self,ISBN,userid,qty,price):        
        cartObj=Cart.objects.filter(ISBN=ISBN,userid_id=userid,sellprice=price).first()
        cartObj.quantity=qty
        cartObj.save()




    def expurgate(self,cartlist):         
        wish=[]                    
        for i in cartlist:                    
            if i['dosell']:                                                                                
                statObj=Status.objects.filter(ISBN=i['ISBN'],sellprice=i['sellprice']).first()                                                

                if statObj.sellquantity == 0:                                                
                    wish.append(i['ISBN'])             
                    self.removeFromCart(i['ISBN'],i['sellprice'])
                    del i                                           
                else:
                    i['quantity']=min(i['quantity'],statObj.sellquantity)
            else:
                statObj=Status.objects.filter(ISBN=i['ISBN'],rentprice=i['sellprice']).first()
                curr=statObj.quantity-statObj.sellquantity                                
                if curr == 0:                        
                    wish.append(i['ISBN'])  
                    self.removeFromCart(i['ISBN'],i['sellprice'])           
                    del i                     
                else:
                    i['quantity']=min(i['quantity'],curr)                    
        return wish,cartlist