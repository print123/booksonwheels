from ..models import User

class UserClass:
	def __init__(self,name,password,email):
		self.name=name
		self.password=password
		self.email=email

	def authenticate(self,isadmin):
		if isadmin==True:
			if self.email=="bow@gmail.com" and self.password=="1234":
				return True
			else:
				return False
		else:
			ans=User.objects.filter(email=self.email,password=self.password)
		if len(ans):
			return True
		else:
			return False

	def addUser(self):
		newuser=User(name=self.name,password=self.password,email=self.email)
		newuser.save()

			

