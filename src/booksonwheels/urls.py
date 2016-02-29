from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
	url(r'^$', 'bow.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login', 'bow.views.login', name='login'),
	#url(r'^cart', 'bow.views.login', name='cart'),
    url(r'^admin/', include(admin.site.urls)),
]
