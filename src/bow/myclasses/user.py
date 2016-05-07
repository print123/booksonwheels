"""A Class that represents a User in the System"""

from ..models import User, Upload,Token
import md5
from random import randint
class UserClass:
    '''def __init__(self, name, password, email, contact_no, address):
        self.name = name
        self.password = password
        self.email = email
        self.address = address
        self.contact_no = contact_no
'''
    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=password

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

    def getId(self, email):
        b = User.objects.filter(email=email).values('userid')
        return b[0]['userid']

    def updatePassword(self,npass):
        m=md5.new()
        m.update(npass)
        User.objects.filter(email=self.email).update(password=m.hexdigest())

    def verifyEmail(self):
        u=None
        try:
            u=User.objects.get(email=self.email)
        except:
            return False
        if u is None:
            return False
        return True

    def sendConfirmMail(self):
        token=self.generateToken(10)
        t=Token(email=self.email,token_gen=str(token))
        t.save()
        self.sendMail(token)

    def generateToken(self,n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def sendMail(self,token):
        import smtplib
        fromaddr = 'booksonwheels8@gmail.com'#sender's email     
        toaddr = self.email #receiver's email
        print self.email
        msg = 'Token for changing password : ' + str(token) 
            
        #gmail credentials
        username = 'booksonwheels8'
        password = 'Programmer@08'
            
        server=smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()

        try:
            server.login(username,password)
            server.sendmail(fromaddr,toaddr,msg)
        except:
            print "not send mail"
            #pass

        server.quit()

    def verifyToken(self,token):
        token_get=None
        print self.email
        try:
            token_get=Token.objects.get(email=self.email,token_gen=token)
        except:
            return False
        if token_get is None:
            return False
        Token.objects.get(email=self.email).delete()
        return True




