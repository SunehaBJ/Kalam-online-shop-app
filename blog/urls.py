#urls for the Blog app.
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views as entry_views
from .forms import SignUpForm,InterestForm,DocumentForm,RatingForm,CommunityForm,AdvertiseForm,DocumentCForm,ProfileForm
form1=SignUpForm()
urlpatterns = [
    url(r'^$', entry_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'extra_context': {'form1':form1 ,},},
         name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', entry_views.signup, name='signup'),
    url(r'^login/interests/$',entry_views.interests,name='interests'),
    url(r'^login/settings/$',entry_views.settings,name='settings'),
    url(r'^login/upfile/$',	entry_views.upfile,name='upfile'),
    url(r'^login/search/$', entry_views.search, name='search'),
    url(r'^login/delete/(?P<pk>\d+)/$', entry_views.delete1, name='delete'),
    url(r'^login/bookpage/(?P<pk>\d+)/$', entry_views.bookpage, name='bookpage'),
    url(r'^login/reset/$',entry_views.reset,name='reset'),
    url(r'^login/editprofile/$',entry_views.editprofile,name='editprofile'),
    url(r'^login/genre/(?P<pk>\w+)/$',entry_views.genre,name='genre'),
    url(r'^login/author/(?P<pk>\w+)/$',entry_views.author,name='author'),
    url(r'^login/uploader/(?P<pk>\w+)/$',entry_views.uploader,name='uploader'),
    url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'password_reset_form.html'},name='password_reset'), 
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm,
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
