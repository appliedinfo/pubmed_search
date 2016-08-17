from django.conf.urls import patterns, include, url
from django.contrib import admin
from abstractsearch.views import SearchView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pubmed_search.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', SearchView.as_view(),name='search'),
)
