from ..models import User,Admin
import string
class AdminClass(UserClass):
	def trackRentRequest(self,date):
		"""A method to get all Rents records on particular date"""
		ans=Rents.object.filter(date_of_issue=date)
		return ans

	def trackOrderRequest(self,date):
		"""A method to get all Order records on particular date"""
		ans=Order.object.filter(date_of_order=date)
		return ans

	def notifyBuyer(self,ISBN):
		"""A method to notify user from wishlist by ISBN"""
		ans=WishList.object.filter(ISBN=ISBN).values('userid')
		import smtp
		fromaddr = 'booksonwheelsteam@gmail.com'#sender's email		
        for id in ans
            mail=User.objects.filter(userid=id).values('email')
            """script for mail goes here"""
		toaddr = mail #receiver's email
		msg = 'Hi there'#The message
			
		#gmail credentials
		username = 'booksonwheelsteam'
		password = 'books^**'
			
		server=smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()


		server.login(username,password)
		server.sendmail(fromaddr,toaddr,msg)

		server.quit()



	def updateBookStatus(self,bookid):
		"""A method to update available status of book by bookid"""
		Book.object.filter(bookid=bookid).update(available=True)
		code=Book.object.filter(bookid=bookid).values('ISBN')
		notifyBuyer(code)