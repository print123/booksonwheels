from django.shortcuts import render
from django.shortcuts import render_to_response
from .myclasses.user import UserClass
from .myclasses.book import BookClass
from .forms import *
from django.http import HttpResponseRedirect
from .myclasses.search import SearchClass
from django.template import RequestContext

# Create your views here.
def home(request):
    books=BookClass().getBooks(3)
    print books
    '''for b in books:
        b.imageurl="{%"+" static"+" '"+b.imageurl+"' %}"
        print b.imageurl'''    
    context = {'books':books}
    return render(request, "index.html", context)


def login(request):
    lform = LoginForm()
    sform = SignUpForm()
    # rform=retype()
    is_not_auth = False

    context = {'form': lform, 'is_not_auth': is_not_auth, 'sform': sform}
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]
        requestuser = UserClass(name="", password=password, email=email)
        if requestuser.authenticate(False) == True:
            context["is_not_auth"] = False
            return HttpResponseRedirect('/cart/')
        else:
            context["is_not_auth"] = True
            return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)


def cart(request):
    return render(request, "cart.html")


def signup(request):
    if request.method == "POST":
        nuser = UserClass(name=request.POST["name"], password=request.POST["password"], email=request.POST["email"])
        try:
            nuser.addUser()
        except:
            return render(request, "u.html")

    return render(request, "r.html")


def search(request):
    if request.method == "POST":
        s=SearchClass()
        print request.POST["stext"]
        res=s.searchOnString(request.POST["stext"])
        #res=s.searchOnTitle(request.POST["stext"])
        context={'result':res}
        print res
        return render_to_response("search.html",RequestContext(request,context))
