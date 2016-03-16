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
            print "hi"
            result = c.displayCart()
            context = {'result': result}
        return render(request, "cart.html", context)
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
        t_isbn=request.POST.get('name',False)
        tosell=request.POST.get('sell',False)
        torent=request.POST.get('rent',False)
        sellprice=request.POST.get('sellprice',False)
        rentprice=request.POST.get('rentprice',False)
        sellquantity=request.POST.get('sellquantity',False)
        rentquantity=request.POST.get('rentquantity',False)
        b=BookClass()
        bookid=b.getBookid(t_isbn)
        if not bookid==-1:
            owner=request.session['userid']
            b.add_seller(bookid,tosell,torent,sellprice,rentprice,int(sellquantity)+int(rentquantity),owner)
            return HttpResponseRedirect("/")

        CustObj=CustomerClass(request.session["userid"])
        lst=CustObj.uploadBook(t_isbn,tosell,torent,sellprice,rentprice,sellquantity,rentquantity)
        need=[]
        for i in lst:
            if lst[i]=='':
                need.append(i)
            else:
                request.session[i]=lst[i]
        print need
        context={'find':need}
        '''for i in lst:
            if not lst[i]=='':
                context[i]=lst[i]'''
        return render(request,"addinfo.html",context)
    else:
        values={}
        for attr in request.GET:
            values[attr]=request.GET[attr]
        CustObj=CustomerClass(request.session["userid"])
        CustObj.addBook(values,request)
        return HttpResponseRedirect("/")


def wishlist(request):
    if request.session["userid"] is not None:
        w=WishlistClass(request.session["userid"])
        res=w.displayWishlist()
        context = {'result': res}
    return render(request, "wishlist.html", context)    

def search(request):
    if request.method == "POST":

        s = SearchClass()
        # print request.POST["stext"]
        request.session["searchtext"] = request.POST["stext"]
        res = s.searchOnString(request.POST["stext"])
        category = BookClass().getCategoryOfRes(res)
        # request.session["resultset"]=res
        # res=s.searchOnTitle(request.POST["stext"])
        context = {'result': res, 'category': category}
        print res
        if len(res) >= 1:
            return render_to_response("search.html", RequestContext(request, context))  # know why this works
        else:
            return render_to_response("404.html", RequestContext(request, context))


def productdetails(request):
    if request.GET["id"] != "":
        b = BookClass()

        res = b.getBook(request.GET["id"])
        context = {'result': res}        
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

        c.addToCart(request.POST["ISBN"])
        context = {}

        return HttpResponseRedirect("/")         
    except:
        return HttpResponseRedirect("/login")

def addToWishlist(request):
    try:
        w=WishlistClass(request.session["userid"])
        w.addToWishlist(request.POST["ISBN"])
        context = {}
        return HttpResponseRedirect("/")
    except:
        return HttpResponseRedirect("/login")

def remove(request):
    try:
        c=CartClass(request.session["userid"])
        print request.GET["bookid"]
        c.removeFromCart(request.GET["bookid"])
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
        print request.GET["ISBN"]
        c.removeFromWishlist(request.GET["ISBN"])
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