from django.conf.urls import include, url
from django.contrib import admin
from adminplus.sites import AdminSitePlus
admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    # Examples:
	url(r'^$', 'bow.views.home', name='home'),
    url(r'^addfeedback', 'bow.views.addfeedback', name='addfeedback'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login', 'bow.views.login', name='login'),
    url(r'^signup', 'bow.views.signup', name='signup'),
    url(r'^getInfo', 'bow.views.getInfo', name='getInfo'),
	url(r'^search', 'bow.views.search', name='search'),	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart', 'bow.views.cart', name='cart'),
    url(r'^productdetails', 'bow.views.productdetails', name='productdetails'),
    url(r'^logout', 'bow.views.logout', name='logout'),
    url(r'^genre', 'bow.views.bookOfGenre', name='genre'),
	url(r'^auto','bow.views.autocomplete',name='autocomplete'),
    url(r'^resgenre', 'bow.views.resOfGenre', name='resgenre'),
    url(r'^addtowishlist', 'bow.views.addToWishlist', name='addtowishlist'),
    url(r'^wltocart', 'bow.views.wlToCart', name='wltocart'),
	url(r'^upload','bow.views.upload',name='upload'),
    url(r'^order','bow.views.order',name='order'),
    url(r'^update','bow.views.update',name='update'),
    url(r'^mybooks','bow.views.displayMyBooks',name='mybooks'),
    url(r'^removefromcart', 'bow.views.remove', name='removefromcart'),
    url(r'^removefromwishlist', 'bow.views.removeFromWishlist', name='removefromwishlist'),
    url(r'^wishlist', 'bow.views.wishlist', name='wishlist'),
    url(r'^select', 'bow.views.select', name='select'),
    url(r'^addinfo', 'bow.views.addInfo', name='addinfo'),
    url(r'^removefrombooks', 'bow.views.removeFromBooks', name='addinfo'),
    url(r'^updn', 'bow.views.updateCart', name='updateCart'),
    url(r'^checkout', 'bow.views.checkout', name='checkout'),
    url(r'^deliver', 'bow.views.deliver', name='deliver'),
    url(r'^invoice', 'bow.views.invoice', name='invoice'),
    url(r'^test', 'bow.views.test', name='test'),
    url(r'^feedback', 'bow.views.feedback', name='feedback'),
    url(r'^comment', 'bow.views.productdetails', name='comment'),
]
