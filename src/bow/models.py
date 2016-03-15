from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
	userid=models.AutoField(primary_key=True)
	name=models.CharField(max_length=120,blank=False,null=False)
	password=models.CharField(max_length=120,blank=False,null=False)
	email=models.EmailField(max_length=254,blank=False,unique=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	contact_no = models.CharField(max_length=15,validators=[phone_regex], blank=True) # validators should be a list
	address=models.CharField(max_length=500,blank=True,null=False)

	def __unicode__(self):
		return self.name

class Wishlist(models.Model):
	userid=models.ForeignKey('User',on_delete=models.CASCADE)
	ISBN=models.CharField(max_length=20,blank=False,null=False)

	#def __unicode__(self):
	#	return self.userid

class Cart(models.Model):
	userid=models.ForeignKey('User',on_delete=models.CASCADE,)
	ISBN=models.CharField(max_length=20,blank=False,null=False)
	quantity=models.DecimalField(max_digits=5,decimal_places=0)

class Upload(models.Model):
	owner_id=models.ForeignKey('User',on_delete=models.CASCADE)
	dosell=models.BooleanField(default=False)
	dorent=models.BooleanField(default=True)
	rentprice=models.DecimalField(max_digits=8,decimal_places=2)
	sellprice=models.DecimalField(max_digits=8,decimal_places=2)
	bookid=models.ForeignKey('Book',on_delete=models.CASCADE)
	qtyuploaded=models.DecimalField(max_digits=8,decimal_places=0)
	qtyavailable=models.DecimalField(max_digits=8,decimal_places=0)

class Book(models.Model):
	bookid=models.AutoField(primary_key=True)
	author=models.CharField(max_length=100)
	ISBN=models.CharField(max_length=20,blank=False,null=False)
	imageurl=models.CharField(max_length=100,blank=False,null=False)
	genre=models.CharField(max_length=20)
	summary=models.CharField(max_length=1000)
	publisher=models.CharField(max_length=50)
	language=models.CharField(max_length=20,default='English')
	rating=models.DecimalField(max_digits=2,decimal_places=1)
	title=models.CharField(max_length=120,blank=False,null=False)
	

	def __unicode__(self):
		return self.title

class Rents(models.Model):
	bookid=models.ForeignKey('Book',on_delete=models.CASCADE)
	ISBN=models.CharField(max_length=20,blank=False,null=False)
	userid=models.ForeignKey('User',on_delete=models.CASCADE)
	paymentid=models.ForeignKey('Payment',on_delete=models.CASCADE)
	date_of_issue=models.DateTimeField(auto_now_add=True)
	date_of_return=models.DateTimeField()
	owner_id=models.CharField(max_length=20)
	quantity=models.DecimalField(max_digits=8,decimal_places=0)

	def __unicode__(self):
		return self.userid

class Order(models.Model):# for every new (owner and book combination) new entry
	orderid=models.AutoField(primary_key=True)
	userid=models.ForeignKey('User',on_delete=models.CASCADE)
	date_of_order=models.DateTimeField(auto_now_add=True)
	paymentid=models.ForeignKey('Payment',on_delete=models.CASCADE)
	bookid=models.ForeignKey('Book',related_name="order_bookid",on_delete=models.CASCADE)
	owner_id=models.CharField(max_length=20)
	quantity=models.DecimalField(max_digits=8,decimal_places=0)

	def __unicode__(self):
		return self.orderid

class Payment(models.Model):
	paymentid=models.AutoField(primary_key=True)
	mode=models.CharField(max_length=2)
	ispending=models.BooleanField(default=True)

	def __unicode__(self):
		return self.paymentid