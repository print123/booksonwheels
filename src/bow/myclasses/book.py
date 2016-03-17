"""A Class for Book"""
from __future__ import unicode_literals
from ..models import Book, Rents, Upload, Status 
from django.db.models import Count, Min


class BookClass:
    def __init__(self, bookid):
        self.bookid = bookid

    def __init__(self):
        bookid = None

    def mark_it_unavailable(self):
        Book.Object.filter(bookid=self.bookid).update(available=False)

    def getSummary(self):
        return Book.object.filter(bookid=self.bookid).values('summary')

    def getTrending(self):
        rentTrend = Book.objects.all().values('ISBN').annotate(total=Count('ISBN')).order_by('-total')[:3]
        res = []
        for i in rentTrend:
            res += self.getBook(i['ISBN'])
        return res

    def getQuotation(self, time_dur):
        # for customer
        base_price = Book.object.filter(bookid=self.bookid).values('actual_price')
        final_price = 0.1 * base_price * cnt

        return final_price

    def getRent(self):
        # for uploader
        base_price = Book.object.filter(bookid=self.bookid).values('actual_price')
        final_price = 0.1 * base_price * cnt

        return final_price

    def getBooks(self, number):
        b = Book.objects.all()[:number]
        return b

    def getBook(self, ISBN):
        b = Book.objects.filter(ISBN=ISBN)[:1]
        #print type(b)
        print b
        return b

    def getCategory(self):
        catCount = Book.objects.all().values('genre').annotate(total=Count('genre'))
        print catCount
        return catCount

    def getCategoryOfRes(self, res):
        gen_counts = []
        for r in res:
            flag = False
            for d in gen_counts:
                if d['genre'] == r.genre:
                    d['total'] += 1
                    flag = True
                    break
            if flag == False:
                gen_counts.append({'genre': r.genre, 'total': 1})
        return gen_counts


    def add_seller(self,bookid,tosell,torent,sellprice,rentprice,quantity,owner):
        if tosell=="on":
            tosell=True
        else:
            tosell=False
        if torent=="on":
            torent=True
        else:
            torent=False
        #book=self.getBook(isbn)

        #bookobj=Book(ISBN=book['ISBN'],author=book['author'],title=book['author'],summary=book['summary'],imageurl=book['imageurl'],genre=book['genre'],publisher=book['publisher'],rating=book['rating'],language=book['language'],)
        upObj=Upload.objects.filter(owner_id_id=owner,bookid_id=bookid).first()

        if upObj is not None:
            if tosell and torent:                                            
                if rentprice == upObj.rentprice and sellprice == upObj.sellprice:
                    upObj.qtyuploaded = upObj.qtyuploaded + 1
                else:
                    nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,qtyuploaded=quantity,qtyavailable=quantity,rentprice=rentprice,sellprice=sellprice)
            elif tosell:
                if sellprice == upObj.sellprice:
                        upObj.qtyuploaded=upObj.qtyuploaded + 1
                else:
                    nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,qtyuploaded=quantity,qtyavailable=quantity,rentprice=rentprice,sellprice=sellprice)
            elif torent:
                if rentprice == upObj.rentprice:
                        upObj.qtyuploaded=upObj.qtyuploaded + 1
                else:
                    nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,qtyuploaded=quantity,qtyavailable=quantity,rentprice=rentprice,sellprice=sellprice)
        else:
            nuser=Upload(bookid_id=bookid,dosell=tosell,dorent=torent,owner_id_id=owner,qtyuploaded=quantity,qtyavailable=quantity,rentprice=rentprice,sellprice=sellprice)
        
        nuser.save()

    def getBookid(self, ISBN):
        b = Book.objects.filter(ISBN=ISBN).values('bookid')
        try:
            return b[0]['bookid']
        except:
            return -1

    def getPrice(self, ISBN):
        price={}
        c = Status.objects.filter(ISBN=ISBN)
        #d = Status.objects.filter(ISBN=ISBN).aggregate(Min('rentprice'))
        #print type(c)
        print "Sessions"
        print c
        minsellprice=9999999999
        minrentprice=9999999999
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
        b = Book.objects.filter(bookid=bookid).values('ISBN')
        try:
            return b[0]['ISBN']
        except:
            return -1    