from django.shortcuts import render
from .myclasses.user import UserClass
from .forms import LoginForm

# Create your views here.
def home(request):
    context={}
    return render(request,"index.html",context)

def login(request):
    lform=LoginForm()
    #sform=SignUpForm1()
    #rform=retype()
    is_not_auth=False

    context={'form':lform,'is_not_auth':is_not_auth}
    if request.method == "POST":
    	form=LoginForm(request.POST)
    	email=request.POST["email"]
    	password=request.POST["password"]
    	requestuser=UserClass(name="",password=password,email=email)
    	if requestuser.authenticate(False)==True:
    		return HttpResponseRedirect('/cart/')
    	else:
    		context["is_not_auth"]=True
    		return render(request,"login.html",context)
    else:
		return render(request,"login.html",context)
