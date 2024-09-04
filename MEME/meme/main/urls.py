from django.urls import path 
from . import views # import views from root dir(main)


urlpatterns = [
    path("", views.home, name="home"), # home route
    path("register/", views.register, name="register"), # register route
    path("login/", views.login, name="login"), # login route
    path("logout/", views.logout, name="logout"),
    path("memes/", views.getmemes, name="name"),
    path("editmeme/", views.editmeme, name="editmeme"),
    path("editmeme_details/", views.editmeme_details, name="editmeme_details")
]