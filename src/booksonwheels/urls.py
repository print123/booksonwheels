from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
	url(r'^$', 'bow.views.home', name='home'),
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
    url(r'^addto', 'bow.views.addToCart', name='addto'),
	url(r'^upload','bow.views.upload',name='upload'),
    url(r'^removefromcart', 'bow.views.remove', name='removefromcart'),
]
