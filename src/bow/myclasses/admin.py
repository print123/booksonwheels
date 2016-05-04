from ..models import User,Rents,Order,Payment,Book,Status,Upload,Wishlist
from .user import UserClass 
from django.db.models import F
from datetime import timedelta
from datetime import datetime
from django.utils import timezone
from couchdb import Server
import string
class AdminClass():
	def trackRentRequest(self):
		"""A method to get all Rents records on particular date"""
		#start_date = timezone.now().date()
		start_dat=datetime.today()
		start_date = start_dat - timedelta( hours=start_dat.time().hour,minutes=start_dat.time().minute,seconds=start_dat.time().second ) 
		end_date=start_dat
		ans=None
		#print start_dat.time().hour
		print end_date
		ans=Rents.objects.filter(date_of_issue__range=(start_date,end_date))
		lst=[]
		for b in ans:
			owneradd=b.owner_id.address
			useradd=b.userid.address
			username=b.userid.email
			ownername=b.owner_id.email
			userphone=b.userid.contact_no
			ownerphone=b.owner_id.contact_no
			bookname=b.bookid.title
			status=b.paymentid.ispending
			book=b.__dict__
			book['owneradd']=owneradd
			book['useradd']=useradd
			book['username']=username
			book['ownername']=ownername
			book['userphone']=userphone
			book['ownerphone']=ownerphone
			book['name']=bookname
			if status==True:
				book['status']="Pending"
			else:
				book['status']="Delivered"
			lst.append(book)
		#print ans
		if ans is None:
			print "not found"
		else:
			print "found"
		return lst
		

	def trackOrderRequest(self):
		"""A method to get all Order records on particular date"""
		start_dat=datetime.today()
		start_date = start_dat - timedelta( hours=start_dat.time().hour,minutes=start_dat.time().minute,seconds=start_dat.time().second ) 
		end_date=start_dat
		ans=None
		#print start_dat.time().hour
		print end_date
		ans=Order.objects.filter(date_of_order__range=(start_date,end_date))
		lst=[]
		for b in ans:
			owneradd=b.owner_id.address
			useradd=b.userid.address
			username=b.userid.email
			ownername=b.owner_id.email
			userphone=b.userid.contact_no
			ownerphone=b.owner_id.contact_no
			bookname=b.bookid.title
			status=b.paymentid.ispending
			book=b.__dict__
			book['owneradd']=owneradd
			book['useradd']=useradd
			book['username']=username
			book['ownername']=ownername
			book['userphone']=userphone
			book['ownerphone']=ownerphone
			book['name']=bookname
			if status==True:
				book['status']="Pending"
			else:
				book['status']="Delivered"
			lst.append(book)
		#print ans
		
		return lst

	def trackReturn(self):
		start_dat=datetime.today()
		start_date = start_dat - timedelta( hours=start_dat.time().hour,minutes=start_dat.time().minute,seconds=start_dat.time().second ) 
		end_date=start_dat
		ans=None
		#print start_dat.time().hour
		print end_date
		ans=Rents.objects.filter(date_of_return__range=(start_date,end_date))
		lst=[]
		for b in ans:
			owneradd=b.owner_id.address
			useradd=b.userid.address
			username=b.userid.email
			ownername=b.owner_id.email
			userphone=b.userid.contact_no
			ownerphone=b.owner_id.contact_no
			bookname=b.bookid.title
			book=b.__dict__
			book['owneradd']=owneradd
			book['useradd']=useradd
			book['username']=username
			book['ownername']=ownername
			book['userphone']=userphone
			book['ownerphone']=ownerphone
			book['name']=bookname
			if book['status']=='p':
				book['status']='pending'
			else:
				book['status']='returned'
			lst.append(book)
		#print ans
		
		return lst

	def notifyBuyer(self,ISBN):
		"""A method to notify user from wishlist by ISBN"""
		ans=Wishlist.objects.filter(ISBN=ISBN).values('userid')
		import smtplib
		fromaddr = 'booksonwheelsteam@gmail.com'#sender's email		
		
		for i in ans:
			mail=None
			print "hi  "
			print i['userid']
			mail=User.objects.filter(userid=i['userid']).values('email')
			print mail
	        """script for mail goes here"""
	        if not mail is None:
				toaddr = mail[0]['email'] #receiver's email
				msg = 'The book is available.Add to cart and checkout as quick as possible.'#The message
					
				#gmail credentials
				username = 'booksonwheelsteam'
				password = 'books^**'
					
				server=smtplib.SMTP('smtp.gmail.com:587')
				server.starttls()

				try:
					server.login(username,password)
					server.sendmail(fromaddr,toaddr,msg)
				except:
					print "not send mail"
					#pass

		server.quit()


	def UpdateStatus(self,pid):
		b1=Rents.objects.filter(paymentid_id=pid).first()
		amount=Payment.objects.filter(paymentid=pid).values('amount')
		b=b1.__dict__
		quant=b['quantity']
		bookid=b['bookid_id']
		price=amount[0]['amount']/quant
		#price=float("{.2f}".format(amount[0]['amount']))/float("{0:.2f}".format(quant))
		Rents.objects.filter(paymentid_id=pid).update(status='r')
		Book.objects.filter(bookid=bookid).update(quantity=F('quantity')+quant)
		Status.objects.filter(ISBN=b['ISBN'],rentprice=price).update(quantity=F('quantity')+quant)
		Upload.objects.filter(owner_id_id=b['owner_id_id'],sellprice=price).update(qtyavailable=F('qtyavailable')+quant)
		self.notifyBuyer(b['ISBN'])

	def getFeedbacks(self):
		couch=Server()
		db=couch['feedback']
		feeds=[]
		for i in db:
			feeds.append(db[i])
			print db[i]
		return feeds
	