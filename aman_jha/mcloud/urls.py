from django.conf.urls import url,include
from mcloud import views

app_name='mcloud'

urlpatterns=[
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^register/$',views.UserFormView.as_view(),name='register'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<album_id>[0-9]+)/favorite/$',views.favorite,name='favorite'),
    url(r'mcloud/add/$',views.Albumcreate.as_view(),name='album-add'),
    url(r'mcloud/album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),
    url(r'mcloud/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
]