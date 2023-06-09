from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="healthapp"),
    path("about/", views.about, name="AboutUs"),
    path("ourservices/", views.ourservices, name="ourservices"),

    path("ourdoctors/", views.ourdoctors, name="ourdoctors"),
    path("consultationform/", views.Consultationform, name="consultation"),
    path("blog/", views.blog, name="blog"),
    path("docview/<int:myid>",views.docview,name='ViewDoctorsProfile'),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout")

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
