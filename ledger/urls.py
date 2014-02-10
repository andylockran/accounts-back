from django.conf.urls import patterns,include,url

urlpatterns = patterns('ledger.views',
      url(r'^$', 'index', name="index"),
      url(r'^submit/$', 'submit', name="submit"),
      )
