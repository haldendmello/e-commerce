from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categorie", views.categorie, name="categorie"),
    path("catlist/<cat>",views.catlist,name="catlist"),
    path("addwatchlist/<listtitle>", views.addwatchlist, name="addwatchlist"),
    path("watchlist",views.watch_list,name="watchlist"),
    path("removewatch/<listtitle>",views.removewatch,name="removewatch"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("wonlisting", views.wonlisting, name="wonlisting"),
    path("listview/<listtitle>",views.listview,name="listview"),
    path("mylisting",views.mylisting,name="mylisting"),
    path("current_bid/<int:listpk>/",views.current_bid,name="current_bid"),
    path("closebid/<int:listpk>",views.closebid,name="closebid"),
    path("comments<listtitle>",views.comments,name="comments"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
