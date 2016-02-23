from ..models import User,Admin

class UserClass:
	def __init__(self,name,password,email):
		self.name=name
		self.password=password
		self.email=email

	def authenticate(self,isadmin):
		if isadmin==True:
			ans=Admin.objects.filter(email=email,password=password)
		else:
			ans=User.objects.filter(email=email,password=password)
		if len(ans):
			return True
		else:
			return False

	def addUser(self):
		newuser=User(name=name,password=password,email=email)
		newuser.save()

			

