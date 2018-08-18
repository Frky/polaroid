from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from website import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create$', views.create_gallery, name="create"),
    url(r'^upload$', views.upload, name="upload"),
    url(r'^gl/(?P<gid>[-A-Za-z0-9_]+)$', views.gallery, name="gallery"),
    url(r'^rm/gl/(?P<gid>[-A-Za-z0-9_]+)$', views.remove_gallery, name="remove_gl"),
    url(r'^rm/img/(?P<mid>[-A-Za-z0-9_]+)$', views.remove_img, name="remove_img"),
    url(r'^crop/img/(?P<mid>[-A-Za-z0-9_]+)$', views.crop, name="crop"),
    url(r'^cover/(?P<gid>[-A-Za-z0-9_]+)$', views.cover_gallery, name="cover"),
    url(r'^name/(?P<gid>[-A-Za-z0-9_]+)$', views.name_gallery, name="name"),
    url(r'^cover/set/(?P<gid>[-A-Za-z0-9_]+)/(?P<mid>[-A-Za-z0-9_]+)$', views.set_cover_gallery, name="set_cover"),
    url(r'^name/set/(?P<gid>[-A-Za-z0-9_]+)$', views.set_name_gallery, name="set_name"),

    url(r'^register$',  views.register, name="register"),
    url(r'^login$',  LoginView.as_view(), name="login"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

