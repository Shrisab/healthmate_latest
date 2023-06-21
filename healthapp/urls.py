from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="healthapp"),
    path("about/", views.about, name="AboutUs"),
    path("ourservices/", views.ourservices, name="Ourservices"),
    path("ourdoctors/", views.ourdoctors, name="ourdoctors"),
    path("consultationform/", views.Consultationform, name="consultation"),
    path("blog/", views.blog, name="blog"),
    path("docview/<int:myid>",views.docview,name='ViewDoctorsProfile'),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path("profile_update/", views.profile_update, name="profile_update"),
    path("profile_view/", views.profile_view, name="profile_view"),
    # path("change_password/",views.change_password,name="change_password")
    path(
        "change_password/",
        auth_views.PasswordChangeView.as_view(
            template_name='healthapp/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    path('blog_home', views.blog_home, name="blog_home"),
    path('post/<int:pk>', views.view_post, name="view-post"),
    path('save_comment/', views.save_comment, name="save-comment"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete-comment")
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
