from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .models import Phone

# Create your views here.

# This function leads to the home page
def home(request):
    return render(request, 'tc/home.html')

# This function handle the signup
def signup(request):
    if request.method=="POST":
        username= request.POST.get("username")
        email= request.POST.get("email")
        pass1= request.POST.get("pass1")
        pass2= request.POST.get("pass2")
        phone= request.POST.get("phonenumber")

        if pass1!=pass2:
            print("The passwords dont match")
            return redirect("home")
        try:
            myuser=User.objects.create_user(username=username, email=email,password=pass1)
            myuser.save()
            myphone=Phone(user=myuser, phone=phone)
            myphone.save()
        except:
            print("some errors")
            return redirect("login")
           
        return render(request, 'tc/login.html')
    else:
        return HttpResponse("404 - Not Found")

#This function handles the login
def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST["loginusername"]
        loginpassword=request.POST["loginpassword"]
        user=authenticate(username=loginusername, password=loginpassword)
        
        if user is not None:
            login(request,user)
            
            return redirect("home")
        else:
            
            return redirect("home")
    return HttpResponse("404 - Not found")

# This function takes to the login page
def gologin(request):
    if request.user.is_authenticated:  return redirect("home")
    return render(request, "tc/login.html")

# This function handles the logout page
def handlelogout(request):
    logout(request)
    return redirect("home")

# Marks the phone number as spam
def issafe(request):
    if request.method=="POST":
        phone= request.POST["phone"]
        issafer=request.POST.get("issafe",None)
        # print(issafe)
        phone=Phone.objects.filter(phone=phone).first()
        if not phone:
            print("not phone")
            return redirect("home")
        if issafer=='False':
            print("I am in False")
            # print(phone.user,phone.is_safe)
            phone.is_safe=False
        else:
            phone.is_safe=True
        
        phone.save()
        return redirect("home")
    return HttpResponse("404 - Not found")

