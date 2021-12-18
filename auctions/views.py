from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from decimal import *
from django.contrib import messages

from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile

def index(request):

    context = {
        'listing' : listing.objects.all()
    }
    return render(request, "auctions/index.html",context)

@login_required(login_url='login')
def categorie(request):
    if request.method == 'GET':
        return render(request,"auctions/categorie.html")
@login_required(login_url='login')
def catlist(request,cat):
    context = {
        'listing' : listing.objects.filter(category=cat)
    }
    return render(request,"auctions/index.html",context)

@login_required(login_url='login')
def watch_list(request):
    context = {
        'watchtitle' : watchlist.objects.filter(user = request.user )
    }
    return render(request,"auctions/watchlist.html",context)
        

@login_required(login_url='login')
def addwatchlist(request,listtitle):
    if request.method == 'POST':
        check = watchlist.objects.filter(user=request.user,watchpage=listing.objects.get(title=listtitle)).exists()
        if check == True :
            messages.success(request,"Item Added Successfully in Watch List")
            return HttpResponseRedirect(reverse('watchlist'))
        else:
            watch_obj = watchlist(user = request.user , watchpage=listing.objects.get(title=listtitle)) 
            watch_obj.save()
            messages.success(request,"Item Added Successfully in Watch List")
            return HttpResponseRedirect(reverse('watchlist'))
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login')
def removewatch(request,listtitle):
    if request.method == 'POST' :
        remove_obj = watchlist.objects.get(pk=listtitle)
        remove_obj.delete()
        messages.success(request,"Item removed from Watch List")
        return HttpResponseRedirect(reverse('watchlist'))

@login_required(login_url='login')
def createlisting(request):
    if request.method == 'POST':
        cate = request.POST["category"] 
        user = request.user
        title = request.POST["title"]
        startbid = request.POST["startbid"]
        imageurl = request.POST["imageurl"]
        description = request.POST["description"]

        

        activelisting = listing(user=user,title=title,category=cate,startbid=startbid,description=description)
        
        if imageurl :
            name = urlparse(imageurl).path.split('/')[-1]
            response = requests.get(imageurl)
            if response.status_code == 200:
                activelisting.listimage.save(name,ContentFile(response.content),save=True)

     
        
        activelisting.save()

        curr_obj = currbid(user = user , listbid= activelisting)
        curr_obj.save()
        messages.success(request,"Item Added Successfully")

        return HttpResponseRedirect(reverse('index'))

    else:    
        
        return render(request,"auctions/createlisting.html")

@login_required(login_url='login')
def current_bid(request,listpk):
    list_obj = listing.objects.get(pk=listpk)
    curr_obj = currbid.objects.get(listbid=list_obj)
    bid = request.POST["bid"]
   
    curr_obj.delete()

    curr_new = currbid(user = request.user , bid = bid , listbid=list_obj)
    curr_new.save()

    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login')
def wonlisting(request):
    context = {
        'listing' : listing.objects.all()
    }
    return render(request,"auctions/wonlisting.html",context)



@login_required(login_url='login')
def listview(request,listtitle):
    context={
        'listtitle' : listing.objects.get(title=listtitle),
        'currentbid' : currbid.objects.get(listbid=listing.objects.get(title=listtitle)),
        'comment' : listcomment.objects.filter(listname=listtitle)
    }
    return render(request,"auctions/listview.html",context)



@login_required(login_url='login')
def mylisting(request):
    context = {
        'listing' : listing.objects.filter(user=request.user)
    }
    return render(request,"auctions/mylisting.html",context)


@login_required(login_url='login')
def closebid(request,listpk):
    close_obj = listing.objects.get(pk = listpk)
    close_obj.status='close'
    close_obj.save()
    messages.success(request,"Item Bid colsed")

    return HttpResponseRedirect(reverse('wonlisting'))


@login_required(login_url='login')
def comments(request,listtitle):
    if request.method == 'POST':
        comment_obj = listcomment(user = request.user , comment= request.POST["comment"] , listname = listtitle)
        comment_obj.save()
        return HttpResponseRedirect(reverse('listview', args=(listtitle,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

