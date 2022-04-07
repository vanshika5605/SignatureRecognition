from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage
# from .models import UserProfile
# Create your views here.

def register(request):
    if request.method == 'POST' and request.FILES['photograph'] and request.FILES['signature']:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        photograph = request.FILES['photograph']
        signature = request.FILES['signature']
        # usertype = request.POST['usertype']
        folder_p='photos/'

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                temp1=username+'_photo.jpg'
                temp2=username+'_sign.jpg'
                fss = FileSystemStorage() #location='/media/photos'
                file = fss.save(temp1, photograph)
                file_url = fss.url(file)

                fss = FileSystemStorage()
                file = fss.save(temp2, signature)
                file_url = fss.url(file)
                # if (usertype==1):
                #     rent=1
                #     thrift=0
                # elif (usertype==2):
                #     rent=0
                #     thrift=1
                # userprofile=UserProfile(is_renter=rent, is_thrifter=thrift)
                # userprofile.save()
                return redirect("login")
        else:
            messages.info(request, 'Password not matched')
            return redirect('/')
        return redirect('/')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect("login")
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')