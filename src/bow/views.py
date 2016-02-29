from django.shortcuts import render
from .myclasses.user import UserClass
from .forms import *
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    context = {}
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


