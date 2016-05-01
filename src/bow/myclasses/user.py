"""A Class that represents a User in the System"""

from ..models import User, Upload
import md5
class UserClass:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def authenticate(self, isadmin):
        """To authentcate Users and also Authorises Users """
        if isadmin == True:
            if self.email == "bow@gmail.com" and self.password == "1234":
                return True
            else:
                return False
        else:
            try:
                m=md5.new()
                m.update(self.password)
                ans = User.objects.get(email=self.email, password=m.hexdigest())
            except:
                return False
            if ans is not None:
                self.userid=ans.userid
                self.name=ans.name
                return True
            else:
                return False

    def addUser(self):
        """To Add New User """
        m=md5.new()
        m.update(self.password)
        print m.hexdigest()
        newuser = User(name=self.name, password=m.hexdigest(), email=self.email)
        newuser.save()