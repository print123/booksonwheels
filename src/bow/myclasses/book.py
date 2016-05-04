"""A Class for Book"""
from __future__ import unicode_literals
from ..models import Book, Rents, Upload, Status , Payment 
from django.db.models import Count, Min



class BookClass:
    def __init__(self, bookid):
        self.bookid = bookid

    def __init__(self):
        bookid = None


    def mark_it_unavailable(self):
        """A method to mark a book unavailable"""
        Book.Object.filter(bookid=self.bookid).update(available=False)

    def getSummary(self):
        """A method to get book summary"""
        return Book.object.filter(bookid=self.bookid).values('summary')

    def getTrending(self):
        """A method to get Current Trending Books in the system"""
        rentTrend = Book.objects.all().values('ISBN').annotate(total=Count('ISBN')).order_by('-total')[:6]
        res = []
        for i in rentTrend:
            res += self.getBook(i['ISBN'])
        return res

    def getQuotation(self, time_dur):        
        base_price = Book.object.filter(bookid=self.bookid).values('actual_price')
        final_price = 0.1 * base_price * cnt

        return final_price

    def getRent(self):
        """A method to get Rent Price of a book"""
        base_price = Book.object.filter(bookid=self.bookid).values('actual_price')
        final_price = 0.1 * base_price * cnt

        return final_price

    def getBooks(self, number):
        """A method to get certain number of books from database"""
        b = Book.objects.all()[:number]
        return b

    def getBook(self, ISBN):
        """A method to get a book using ISBN as parameter"""
        b = Book.objects.filter(ISBN=ISBN)[:1]
        #print type(b)        
        return b

    def getCategory(self):        
        catCount = Book.objects.all().values('genre').annotate(total=Count('genre'))        
        return catCount

    def getCategoryOfRes(self, res):

        gen_counts = []
        #t = 0
        for r in res:
            flag = False
            for d in gen_counts:
                if d['genre'] == r['genre']:
                    d['total'] += 1
                    #t += 1
                    flag = True
                    break
            if flag == False:
                #t += 1
                gen_counts.append({'genre': r['genre'], 'total': 1})
        return gen_counts

    def getNumberOfRes(self, res):
        gen_counts = []
        t = 0
        for r in res:
            flag = False
            for d in gen_counts:
                if d['genre'] == r['genre']:
                    d['total'] += 1
                    t += 1
                    flag = True
                    break
            if flag == False:
                t += 1
                gen_counts.append({'genre': r['genre'], 'total': 1, 'tot': t})
        return t


    def add_seller(self,bookid,tosell,torent,sellprice,rentprice,sellquantity,quantity,owner):                
        """A method to update database and insert an entry for the owner of the book."""
        upObj=Upload.objects.filter(owner_id_id=owner,bookid_id=bookid).first()                
        if upObj is not None:            
            if tosell and torent:                                            
                if int(rentprice) == int(upObj.rentprice) and int(sellprice) == int(upObj.sellprice):
                    upObj.sqtyuploaded=upObj.sqtyuploaded+sellquantity
                    upObj.qtyuploaded = upObj.qtyuploaded + quantity
                    upObj.qtyavailable=upObj.qtyavailable + quantity
                    upObj.sqtyavailable=upObj.sqtyavailable+sellquantity
                    upObj.dosell=tosell
                    upObj.dorent=torent
                else:
                    nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,sqtyuploaded=sellquantity,qtyuploaded=quantity,qtyavailable=quantity,sqtyavailable=sellquantity,rentprice=rentprice,sellprice=sellprice)
                    nuser.save()
            elif tosell:
                if int(sellprice) == int(upObj.sellprice):
                    upObj.sqtyuploaded=upObj.sqtyuploaded+sellquantity
                    upObj.qtyuploaded=upObj.qtyuploaded + quantity
                    upObj.qtyavailable=upObj.available+quantity
                    upObj.sqtyavailable=upObj.sqtyavailable+sellquantity
                    upObj.dosell=tosell                    
                else:
                    nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,sqtyuploaded=sellquantity,qtyuploaded=quantity,qtyavailable=quantity,sqtyavailable=sellquantity,rentprice=rentprice,sellprice=sellprice)
                    nuser.save()
            elif torent:
                if int(rentprice) == int(upObj.rentprice):
                    upObj.qtyavailable=upObj.qtyavailable + quantity
                    upObj.qtyuploaded=upObj.qtyuploaded + quantity
                    upObj.dorent=torent
                else:
                    nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,sqtyuploaded=sellquantity,qtyuploaded=quantity,qtyavailable=quantity,sqtyavailable=sellquantity,rentprice=rentprice,sellprice=sellprice)
                    nuser.save()
            upObj.save()    
        else:            
            nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,sqtyuploaded=sellquantity,qtyuploaded=quantity,qtyavailable=quantity,sqtyavailable=sellquantity,rentprice=rentprice,sellprice=sellprice)
            nuser.save()
        
        

    def getBookid(self, ISBN):
        """A method to get ID of the book from ISBN"""
        b = Book.objects.filter(ISBN=ISBN).values('bookid')
        try:
            return b[0]['bookid']
        except:
            return -1

    def getPrice(self, ISBN):
        """A method to get price of the book to display"""
        price={}
        c = Status.objects.filter(ISBN=ISBN)
        #d = Status.objects.filter(ISBN=ISBN).aggregate(Min('rentprice'))
        #print type(c)        
        minsellprice=999999
        minrentprice=999999
        for i in c:
            if i.sellprice < minsellprice and i.sellquantity>0: 
                minsellprice=i.sellprice
            if i.rentprice<minrentprice and i.quantity-i.sellquantity>0:
                minrentprice=i.rentprice
        price['rentprice']=minrentprice
        price['sellprice']=minsellprice
        #print c['ISBN']
        #print type(c)
        #print d
        
        #price['sellprice'] = c['sellprice']
        #price['rentprice'] = d['rentprice']
        return price

    def getISBN(self, bookid):
        """A method to get ISBN of the book from bookid"""
        b = Book.objects.filter(bookid=bookid).values('ISBN')
        try:
            return b[0]['ISBN']
        except:
            return -1    

    def getOwner(self,bookid,quantity,dosell,price):
        """A method to get owner of the book"""
        if dosell:
            upObj=Upload.objects.filter(bookid_id=bookid,dosell=dosell,sellprice=price).first()
            if upObj.qtyuploaded > 0:
                retOwnid=upObj.owner_id_id
                if upObj.sqtyavailable >= quantity:
                    #upObj.sqtyuploaded=upObj.sqtyuploaded-quantity
                    upObj.sqtyavailable=upObj.sqtyavailable-quantity
                    upObj.qtyavailable=upObj.qtyavailable-quantity
                    quantity=0                    
                else:
                    upObj.qtyavailable=upObj.qtyavailable-upObj.sqtyavailable
                    quantity=quantity-upObj.sqtyavailable
                    upObj.sqtyuploaded=0                    
                upObj.save()                
                return (retOwnid,quantity)
                            
        else:
            upObj=Upload.objects.filter(bookid_id=bookid,dorent=True,rentprice=price).first()
            curr=upObj.qtyavailable-upObj.sqtyavailable
            if curr > 0:
                retOwnid=upObj.owner_id_id
                if curr >= quantity:
                    upObj.qtyavailable=upObj.qtyavailable-quantity
                    quantity=0
                else:
                    upObj.qtyavailable=upObj.qtyavailable-(curr)
                    quantity=quantity-curr                    
                upObj.save()
                return (retOwnid,quantity)

    def UpdatePayStatus(self,pid):
        Payment.objects.filter(paymentid=pid).update(ispending=False)   
