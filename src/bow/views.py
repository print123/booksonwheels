from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from .myclasses.order import OrderClass
from .myclasses.user import UserClass
from .myclasses.book import BookClass
from .myclasses.cart import CartClass
from .myclasses.wishlist import WishlistClass
from .myclasses.customer import CustomerClass
from .forms import *
from django.http import HttpResponseRedirect,HttpResponse
from .myclasses.search import SearchClass
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from couchdb import Server
from datetime import datetime



# Create your views here.

@csrf_exempt

def autocomplete(request):
    print "In autocomplete"
    s = SearchClass()
    simple_qs = s.searchToSuggest(request.GET["stext"])
    #results = ['starting']
    print simple_qs
    results=[]
    for r in simple_qs:
        #print r['title']
        del r['sprice']
        del r['rprice']
        del r['sellquantity']
        del r['quantity']
        del r['rating']
        del r['_state']
        results.append(r['title'])
    #resp = request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
    resp = json.dumps(results,sort_keys=True,indent=4, separators=(',', ': '))
    #print resp
    return HttpResponse(resp, content_type='application/json')

    

def home(request):
    books = BookClass().getTrending()
    category = BookClass().getCategory()
    context = {'books': books, 'category': category}
    return render(request, "index.html", context)

def test(request):
    return render(request, "type.html")
    
def login(request):
    try:
        if request.session["userid"] is not None:
            return HttpResponseRedirect('/')
    except:
        already_login = True

    lform = LoginForm()
    # sform = SignUpForm()
    # rform=retype()
    is_not_auth = False

    context = {'form': lform, 'is_not_auth': is_not_auth}
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]
        requestuser = UserClass(name="", password=password, email=email)
        if requestuser.authenticate(False) == True:
            context["is_not_auth"] = False
            request.session["userid"] = requestuser.userid
            request.session["name"] = requestuser.name
            
            cartObj=CartClass(requestuser.userid)
            l=cartObj.getTotal()            
            request.session["cartquant"]=l
                
            wishObj=WishlistClass(requestuser.userid)
            x=wishObj.getTotal()
            request.session["wishquant"]=x

            return HttpResponseRedirect('/')
        else:
            context["is_not_auth"] = True            
            return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)

def signup(request):
    if request.method == "POST":
        address=request.POST.get('address') + "|" + request.POST.get('city') + "|" + request.POST.get('code')
        nuser = UserClass(name=request.POST["name"], password=request.POST["password1"], email=request.POST["email"], address=address, contact_no=request.POST["contact"])
        try:         
            nuser.addUser()            
        except Exception as e:
                print e

    return HttpResponseRedirect("/")


def cart(request):
    try:        
        if request.session["userid"] is not None:            
            c = CartClass(request.session["userid"])                        
            result = c.displayCart()                  
            total=0            
            for r in result:
                if r['timeperiod']==0:                   
                    total += r['quantity'] * r['sellprice']                
                else:                    
                    total += r['quantity'] * r['sellprice']*r['timeperiod']                

        try:
            if request.session["added"] is not None:            
                context = {'result': result, 'total': total,'added':True}
                del request.session["added"]                    
            return render(request, "cart.html", context)
        except Exception as ex:            
            context = {'result': result, 'total': total,'added':False}            
            return render(request, "cart.html", context)
    except Exception as t:        
        return HttpResponseRedirect("/login")

def wishlist(request):
    try:
        if request.session["userid"] is not None:
            w=WishlistClass(request.session["userid"])
            res=w.displayWishlist()
        try:
            if request.session["addedW"] is not None:
                context = {'result': res,'addedW':True}
                del request.session["addedW"]                
            return render(request,"wishlist.html",context)
        except:
            context={'result':res,'addedW':False}            
            return render(request,"wishlist.html",context)
    except:
        return HttpResponseRedirect("/")    

def upload(request):
    try:
        if request.session["userid"] is not None:            
            return render(request,"upload.html")
    except:
        return HttpResponseRedirect("/")

def order(request):
    try:
        if request.session["userid"] is not None:
            
            obj = OrderClass(request.session["userid"])
            result = obj.displayOrders()
            
            context = {'result': result}        
            return render(request,"order.html",context)
    except:
        return HttpResponseRedirect("/")

def getInfo(request):
    if request.method=="POST":
        t_isbn=request.POST.get('name')
        b=BookClass()
        bookid=b.getBookid(t_isbn)        
        need=[]
        got={}
        cartObj = CartClass(request.session["userid"])
        cust = cartObj.getCust()
        if cust.address is not None:
            array = cust.address.split("|")
            a = array[0]
            b = array[1]
            c = array[2] 
        flag=False
        if not bookid==-1:
            owner=request.session['userid']                    
            custObj=CustomerClass(owner)            
            bookObj=BookClass()
            b1=bookObj.getBook(t_isbn)
            request.session["ISBN"]=t_isbn  
            got['ISBN']=t_isbn
            b=b1[0]          
            author=b.author
            request.session['author']=author
            got['author']=author
            imageurl=b.imageurl
            request.session['imageurl']=imageurl
            got['imageurl']=imageurl
            print imageurl
            genre=b.genre
            request.session['genre']=genre
            got['genre']=genre
            summary=b.summary
            request.session['summary']=summary
            got['summary']=summary
            publisher=b.publisher
            request.session['publisher']=publisher
            got['publisher']=publisher
            language=b.language
            request.session['language']=language
            got['language']=language
            title=b.title            
            request.session['title']=title
            got['title']=title
            rating=4.0
            request.session['old']=True              
        else:
            CustObj=CustomerClass(request.session["userid"])
            lst=CustObj.uploadBook(t_isbn,got)
            
            
            for i in lst:
                if lst[i]=='' and not i=='imageurl':
                    need.append(i)
                elif i=='imageurl' and lst[i]=='':
                    flag=True
                else:                    
                    request.session[i]=lst[i]
        #print need
        context={'got':got,'find':need,'ISBN':t_isbn,'cust': cust, 'a': a, 'b': b, 'c': c}

        
        if flag==True:
            context['imageurl']=True
            uform=UploadForm()
            context['uform']=uform
        return render(request,"addinfo.html",context)
        

def addInfo(request):
    if request.method=="POST":
        t_sell=request.POST.get('sell')
        if t_sell == 'on':
            tosell=True
        else:
            tosell=False
        t_rent=request.POST.get('rent')        
        if t_rent =='on':
            torent=True
        else:
            torent=False
        t_list=[]                          
        doc={'_id':request.POST['ISBN'],'comments':t_list}
        server=Server()
        db=server['reviews']   
        temp=db.get(request.POST['ISBN'])             
        if temp is None:
            db.save(doc)
        sellprice=request.POST.get('sellprice')
        rentprice=request.POST.get('rentprice')
        sellquantity=request.POST.get('sellquantity')
        t_ISBN=request.POST.get('ISBN')        
        rentquantity=request.POST.get('rentquantity')
        if 'imageurl' in request.POST:
            form=UploadForm(request.POST,request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'],request.POST['ISBN'])
            values={}
            values['imageurl']='images/'+request.POST['ISBN']+'.jpg'            
            for attr in request.POST:
                if not (attr=="imageurl" or attr=="ISBN"):                    
                    values[attr]=request.POST[attr]
            CustObj=CustomerClass(request.session["userid"])
            CustObj.addBook(values,request)
            url="/productdetails?id="+t_ISBN
            request.session["notify"]=True
            return HttpResponseRedirect(url)
        else:
            values={}
            for attr in request.POST:
                values[attr]=request.POST[attr]
            CustObj=CustomerClass(request.session["userid"])
            CustObj.addBook(values,request)
            url="/productdetails?id="+t_ISBN
            request.session["notify"]=True
            return HttpResponseRedirect(url)

def handle_uploaded_file(f,isbn):
    d='bow/static/images/'+isbn+'.jpg'
    destination = open(d, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
   

def search(request):
    if request.method == "POST":
        s = SearchClass()
        request.session["searchtext"] = request.POST["stext"]
        res = s.searchOnString(request.POST["stext"])
        category = BookClass().getCategoryOfRes(res)
        ttl = BookClass().getNumberOfRes(res)
        '''
        i=-1
        for c in category:
            i += 1
        ttl = category[i]['tot']
        '''
        context = {'result': res, 'category': category, 'ttl': ttl}
        
        try:
            return render_to_response("search.html", RequestContext(request, context))  # know why this works
        except:
            return render_to_response("404.html", RequestContext(request, context))

def productdetails(request):
    context={}    
    if request.method == 'GET':        
        if request.GET["id"] != "":
            b = BookClass()
            b1 = BookClass()        
            res = b.getBook(request.GET["id"])
            price = b1.getPrice(request.GET["id"])
            sellp = price['sellprice']
            rentp = price['rentprice']
            addto=False
            try:
                if request.session["notify"] is not None:
                    del request.session["notify"] 
                    addto=True
            except:
                addto=False        


            if sellp==999999:
                context = {'result': res, 'rentp': rentp}
            elif rentp==999999:
                context = {'result': res, 'sellp': sellp}
            else:
                context = {'result': res, 'rentp': rentp,'sellp':sellp}   
            couch=Server()
            db=couch['reviews']     
            doc=db[request.GET['id']]
            doc=doc['comments']            
            doc=doc[-5:]
            
            mydict={'addto':addto,'comment':doc}        
            context.update(mydict)        
            return render_to_response("product-details.html", RequestContext(request, context))
    else:        
        couch=Server()    
        db=couch['reviews']              
        doc=db[request.POST.get('ISBN')]#["ISBN"]]
        comm={'name':request.session['name'],'rtext':request.POST.get('revw')}        
        if doc['comments'] is not None:            
            doc['comments'].append(comm)                        
        else:
            doc['comments']=[]            
            doc['comments'].append(comm)
        db.save(doc)
        return HttpResponseRedirect("/productdetails?id="+request.POST.get('ISBN')) 

def logout(request):
    del request.session["userid"]
    del request.session["name"]
    return HttpResponseRedirect('/')


def bookOfGenre(request):
    if request.GET["genre"] is not None:
        res = SearchClass().searchOnGenre(request.GET["genre"])
        context = {'result': res}        
        return render_to_response("genre.html",RequestContext(request,context))


def resOfGenre(request):
    #print request.GET["genre"]
    if (request.GET["genre"] != 'Sell' and request.GET["genre"] != 'Rent'):
        res = SearchClass().searchResOnGenre(request.GET["genre"], request.session["searchtext"])
        context = {'result': res}
        print len(res)
        return render_to_response("genre.html",RequestContext(request,context))    
    elif request.GET["genre"] == 'Sell':
        s=True
        res = CustomerClass(request.session['userid']).showCategory(s)
        context = {'result': res}
        return render_to_response("genre.html",RequestContext(request,context))
    elif request.GET["genre"] == 'Rent':
        s=False
        res = CustomerClass(request.session['userid']).showCategory(s)
        context = {'result': res}
        return render_to_response("genre.html",RequestContext(request,context))

def addToCart(request):
    try:

        c=CartClass(request.session["userid"])
        dosell=False
        price=0
        timeperiod=0
        if 'group1' in request.POST:
            if request.POST["group1"]=="sell":
                dosell=True
                print "Dosell"
                price=request.POST["sellprice"]
            else:
                price=request.POST["rentprice"]
                timeperiod=request.POST["time"]
        quantity=request.POST['quantity']        
        c.addToCart(request.POST["ISBN"],quantity,dosell,price,timeperiod)        
        context = {}
        temp=request.session["cartquant"]+1
        request.session["cartquant"]=temp
        request.session["added"]=True        
        return HttpResponseRedirect("/cart")         

    except:
        return HttpResponseRedirect("/login")

def wlToCart(request):    
    return HttpResponseRedirect("/productdetails?id="+request.POST.get('ISBN')) 




def addToWishlist(request):
    try:
        w=WishlistClass(request.session["userid"])
        i=w.addToWishlist(request.POST["ISBN"])
        context = {}                
        temp=request.session["wishquant"]+i
        request.session["wishquant"]=temp
        request.session["addedW"]=True
        return HttpResponseRedirect("/wishlist")
    except:
        return HttpResponseRedirect("/login")

def removeFromBooks(request):
    try:        
        bookid=request.POST["id"]        
        custObj=CustomerClass(request.session["userid"])        
        custObj.removeBook(bookid)        
        return HttpResponseRedirect("/mybooks")
    except:
        return HttpResponseRedirect("/login")

def updateQuantity(request):
    try:        
        bookid=request.POST["id"]                    
        ISBN=request.POST["ISBN"]
        if request.POST["sellprice"] is not None:
            sellprice=request.POST["sellprice"]
        else:
            sellprice=0
        if request.POST["sellquant"] is not None:
            sellquant=request.POST["sellquant"]
        else:
            sellquant=0
        
        if request.POST["rentprice"] is not None:
            rentprice=request.POST["rentprice"]
        else:
            rentprice=0        
        if request.POST["rentquant"] is not None:
            rentquant=request.POST["rentquant"]
        else:
            rentquant=0                
        custObj=CustomerClass(request.session["userid"])                
        custObj.updateQuantity(bookid,ISBN,sellprice,rentprice,sellquant,rentquant)       
        return HttpResponseRedirect("/mybooks")
    except Exception as ex:
        print ex
        print "am i here"
        return HttpResponseRedirect("/login")

def remove(request):
    try:
        c=CartClass(request.session["userid"])
        c.removeFromCart(request.GET["ISBN"],request.GET["sellprice"])
        temp=request.session["cartquant"]-1
        request.session["cartquant"]=temp
        return HttpResponseRedirect("/cart")

    except:
        return HttpResponseRedirect("/login")            


def displayMyBooks(request):
    CustObj=CustomerClass(request.session["userid"])
    result=CustObj.myBooks()
    category = CustObj.getCategoryOf(result)
    context={'result':result, 'category':category}
    return render(request,"mybooks.html",context)


def removeFromWishlist(request):
    try:
        c=WishlistClass(request.session["userid"])        
        c.removeFromWishlist(request.GET["ISBN"])
        temp=request.session["wishquant"]-1
        request.session["wishquant"]=temp
        return HttpResponseRedirect("/wishlist")
    except:
        return HttpResponseRedirect("/login")                    

def select(request):
    if request.method=="POST":
        if 'cart' in request.POST:
            return addToCart(request)
        elif 'wishlist' in request.POST:
            return addToWishlist(request)
        else:
            addToCart(request)
            return checkout(request)
    return HttpResponseRedirect('/')

def update(request):
    if request.method == 'POST':
        if 'update' in request.POST:            
            return updateQuantity(request)
        elif 'remove' in request.POST:
            return removeFromBooks(request)
    
    return HttpResponseRedirect('/')

def updateCart(request):
  #  try:
    if request.method == 'POST':
        cartObj=CartClass(request.session["userid"])   
        for i in request.POST:
            print i            
        if int(request.POST["quantity"])==0:
            cartObj.removeFromCart(request.POST["name"],request.POST["price"])
        else:
            cartObj.update(request.POST["name"],request.session["userid"],int(request.POST["quantity"]),request.POST["price"])                    
        return HttpResponseRedirect("/cart")            
   # except:
    #    return HttpResponseRedirect("/cart")


@csrf_exempt
def checkout(request):
    try:        
        if request.session["userid"] is not None:
            uid=request.session["userid"]
            cartObj = CartClass(uid)    
            cust = cartObj.getCust() 
            array = cust.address.split("|")
            a = array[0]
            b = array[1]
            c = array[2]
            result = cartObj.displayCart()              
            temp,result=cartObj.expurgate(result)                                                            
            wishObj=WishlistClass(uid)                        
            for i in temp:
                wishObj.addToWishlist(i)
            price=[]
            total=0
            for r in result:
                if r['timeperiod']==0:
                    total += r['quantity'] * r['sellprice']                
                    price.append(r['quantity'] * r['sellprice'])
                else:
                    total += r['quantity'] * r['sellprice']*r['timeperiod']                
                    price.append(r['quantity'] * r['sellprice']*r['timeperiod'])
                context = {'result': result, 'total': total, 'cust': cust, 'a': a, 'b': b, 'c': c}
            #print cust.email
            return render(request, "checkout.html", context)        
    except:
        return HttpResponseRedirect("/login")


@csrf_exempt
def deliver(request):
    try:
        if request.session["userid"] is not None:                
            contactNo=request.POST.get('contact')              
            address=request.POST.get('address') + "|" + request.POST.get('city') + "|" + request.POST.get('code')
            custObj = CustomerClass(request.session["userid"])            
            custObj.addDeliveryDetails(contactNo,address)
            return HttpResponseRedirect("/checkout")
    except:
        return HttpResponseRedirect("/login")


@csrf_exempt
def pickup(request):
    try:
        if request.session["userid"] is not None:                
            contactNo=request.POST.get('contact')              
            address=request.POST.get('address') + "|" + request.POST.get('city') + "|" + request.POST.get('code')
            custObj = CustomerClass(request.session["userid"])            
            custObj.addDeliveryDetails(contactNo,address)
            return render(request,"addinfo.html")
    except Exception as ex:
        print ex
        return HttpResponseRedirect("/login")              
@csrf_exempt
def invoice(request):
    try:        
        if 'confirm' in request.POST:
            custObj = CustomerClass(request.session["userid"])        
            custObj.bookCheckout()             
            return HttpResponseRedirect("/orders")
        else:
            return HttpResponseRedirect("/cart")
    except:
        return HttpResponseRedirect("/cart")

def addfeedback(request):
    if request.method=="POST":
        emailid=request.POST['emailid']
        feed=request.POST['feedback']
        couch=Server()    
        db=couch['feedback']
        doc={'emailid':emailid,'feedback':feed,'datetime':str(datetime.now())}
        db.save(doc)
    return HttpResponseRedirect("/")
    