from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from .myclasses.user import UserClass
from .myclasses.book import BookClass
from .myclasses.cart import CartClass
from .myclasses.wishlist import WishlistClass
from .myclasses.customer import CustomerClass
from .forms import *
from django.http import HttpResponseRedirect
from .myclasses.search import SearchClass
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def autocomplete(request):
    print "In autocomplete"
    s = SearchClass()
    simple_qs = s.searchOnString(request.GET["stext"])
    results = ['starting']
    for r in simple_qs:
        results.append(r.title)
    resp = request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
    print resp
    return HttpResponse(resp, content_type='application/json')


def home(request):
    books = BookClass().getTrending()
    category = BookClass().getCategory()
    context = {'books': books, 'category': category}
    return render(request, "index.html", context)

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
        nuser = UserClass(name=request.POST["name"], password=request.POST["password1"], email=request.POST["email"])
        try:
            nuser.addUser()            
        except:
               return render(request, "u.html")

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
        except:            
            context = {'result': result, 'total': total,'added':False}                    
            return render(request, "cart.html", context)
    except:
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

def getInfo(request):
    if request.method=="POST":
        t_isbn=request.POST.get('name')
        b=BookClass()
        bookid=b.getBookid(t_isbn)        
        need=[]
        flag=False
        if not bookid==-1:
            owner=request.session['userid']                    
            custObj=CustomerClass(owner)            
            bookObj=BookClass()
            b1=bookObj.getBook(t_isbn)
            request.session["ISBN"]=t_isbn  
            b=b1[0]          
            author=b.author
            request.session['author']=author
            imageurl=b.imageurl
            request.session['imageurl']=imageurl
            genre=b.genre
            request.session['genre']=genre
            summary=b.summary
            request.session['summary']=summary
            publisher=b.publisher
            request.session['publisher']=publisher
            language=b.language
            request.session['language']=language
            title=b.title
            request.session['title']=title
            rating=4.0
            request.session['old']=True              
        else:
            CustObj=CustomerClass(request.session["userid"])
            lst=CustObj.uploadBook(t_isbn)
            
            
            for i in lst:
                if lst[i]=='' and not i=='imageurl':
                    need.append(i)
                elif i=='imageurl' and lst[i]=='':
                    flag=True
                else:
                    print i
                    request.session[i]=lst[i]
        #print need
        context={'find':need,'ISBN':t_isbn}

        
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
            print values['imageurl']
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
    d='C:\\Users\\shunakthakar\\SDP\\booksonwheels\\src\\bow\\static\\images\\'+isbn+'.jpg'
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
    if request.GET["id"] != "":
        b = BookClass()
        b1 = BookClass()
        print request.GET["id"]
        res = b.getBook(request.GET["id"])
        #isbn = b.getISBN(request.GET["id"])
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
        mydict={'addto':addto}
        context.update(mydict)        
        return render_to_response("product-details.html", RequestContext(request, context))


def logout(request):
    del request.session["userid"]
    del request.session["name"]
    return HttpResponseRedirect('/')


def bookOfGenre(request):
    if request.GET["genre"] is not None:
        res = SearchClass().searchOnGenre(request.GET["genre"])
        context = {'result': res}
        print len(res)
        return render_to_response("genre.html",RequestContext(request,context))


def resOfGenre(request):
    if request.GET["genre"] is not None:
        res = SearchClass().searchResOnGenre(request.GET["genre"], request.session["searchtext"])
        context = {'result': res}
        print len(res)
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
        HttpResponseRedirect("/login")

def wlToCart(request):
    c=CartClass(request.session["userid"])
    b=BookClass()
    dosell = True
    quantity=1
    print "1"
    print request.POST["ISBN"]
    print "2"
    timeperiod=1
    price=b.getPrice(request.POST["ISBN"])
    if price['rentprice']< price['sellprice']:
        c.addToCart(request.POST["ISBN"],quantity,dosell,price['rentprice'],timeperiod)
    else:
        c.addToCart(request.POST["ISBN"],quantity,dosell,price['sellprice'],timeperiod)   
    context = {}
    temp=request.session["cartquant"]+1
    request.session["cartquant"]=temp
    return HttpResponseRedirect("/")

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
    context={'result':result}
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
        else:
            return addToWishlist(request)

    return HttpResponseRedirect('/')
