from django.contrib import admin
from django.shortcuts import render
from .myclasses.admin import AdminClass
from .myclasses.book import BookClass
from datetime import datetime

from django.http import HttpResponseRedirect
# Register your models here.
def my_view(request, *args, **kwargs):
	obj=AdminClass()
	print "here"
	rent=obj.trackRentRequest()
	order=obj.trackOrderRequest()
	returnbooks=obj.trackReturn()
	feedbacks=obj.getFeedbacks()
	context={'rent':rent,'order':order,'returnbooks':returnbooks,'feed':feedbacks}
	return render(request, "admin.html",context)

def todeliver(request, *args, **kwargs):
	Bookobj=BookClass()
	for pid in request.POST:
		if request.POST[pid]=="on":
			Bookobj.UpdatePayStatus(int(pid))
	return HttpResponseRedirect("/admin/tracking")

def doreturn(request, *args, **kwargs):
	obj=AdminClass()
	for pid in request.POST:
		print pid
		if request.POST[pid]=="on":
			obj.UpdateStatus(int(pid))
	return HttpResponseRedirect("/admin/tracking")

admin.site.register_view('tracking', view=my_view)
admin.site.register_view('todeliver',view=todeliver)
admin.site.register_view('doreturn',view=doreturn)
