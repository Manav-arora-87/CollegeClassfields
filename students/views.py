from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
import bcrypt
from students.models import Students,Products

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
# from validate_email import validate_email
from django.contrib.auth.models import User
from datetime import *
import uuid , os
domain={'mitsgwl.ac.in','sgsits.ac.in'}


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()       
 
# Create your views here.
def StudentLogin(request):
    try:
        result = request.session['student']
        return redirect("student-dashboard")
    except Exception as e:
        return render(request,'login.html')

def Logout(request):
    request.session.flush()
    return render(request,'home.html')

def CheckStudentLogin(request):
    

    try:
        emailid = request.POST['emailid']
        print(emailid)
        password = request.POST['password']
        admin=Students.objects.get(emailid=emailid)
        print(admin)
        # # Adminlogins.ob
        if bcrypt.checkpw(password.encode("utf8"), admin.password.encode("utf8")):
             request.session['student']=admin.id
             return redirect('student-dashboard')
        else:
            return render(request, "Login.html")
        

    except Exception as e:
          print(e)  
          Logout(request) 
          return render(request, "home.html", {'msg': 'Server Error'})

def Studentdashboard(request):
    
    try:
        
        result = request.session['student']
        products=reversed(Products.objects.all())
        

        return render(request, "Dashboard.html",{'products':products})

    
    except  Exception as e:
        print(e)
        Logout(request) 
        return redirect('student-login')



def BuySell(request):
    
    try:
        result = request.session['student']

        return render(request, "Buyandsell.html",{'result':result})

    
    except  Exception as e:
        print(e)
        Logout(request) 
        return redirect('student-login')


def Chat(request,id):
    
    try:
        result = request.session['student']
        res=Products.objects.get(id=id)
        
        student=Students.objects.get(id=result)
        return render(request, "chat.html",{'student':student,'res':res})

    
    except  Exception as e:
        print(e)
        # Logout(request) 
        return redirect('student-login')




def Productsubmit(request):
    
    try:
        result = request.session['student']
        name = request.POST['name']
        description = request.POST['desc']
        price = request.POST['price']
        productage = request.POST['productage']
        img = request.FILES['productimg']
        filename = str(uuid.uuid4())+img.name[img.name.rfind('.'):]
        t=Products.objects.create(img=filename,productname=name,productdesc=description,price=price,productage=productage,studentid_id=result)
        t.save()
        F = open('F:/clg_classifieds/assets/productimg/'+filename,"wb")
        for chunk in img.chunks():
            F.write(chunk)
            F.close()
        print(name,description,price,productage,img)
        return redirect('student-buysell')


    
    except  Exception as e:
        print(e)
        # Logout(request) 
        return redirect('student-login')




def Registeration(request):
   try: 
    clgemail = request.POST['email']
    
    last= clgemail.split('@')
    if last[1] not in domain:
         return JsonResponse({"error": "Your coleege is not yet registered !!!"}, status=400)
        
    pwd = request.POST['password']
    name= request.POST['name']
    branch= request.POST['branch']
    year= request.POST['year']
    address= request.POST['address']
    
    salt= bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd.encode("utf8"),salt)
    hashed=(hashed.decode("utf8"))
    t=Students.objects.create(emailid=clgemail,is_active=0,password=hashed,name=name,branch=branch,address=address,year=year) #clgid needs to be removed
    t.save()
    current_site = get_current_site(request)
    email_subject = 'Active your Account'
    message = render_to_string('auth/activate.html',
                                   {
                                       'user': t,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(t.pk)),
                                       'token': generate_token.make_token(t)
                                   }
                                   )

    email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [clgemail]
        )

    EmailThread(email_message).start()
    messages.add_message(request, messages.SUCCESS,
                             'account created succesfully')

    return redirect('student-login') 
   except Exception as e:
     print (e)
     return JsonResponse({"error": "Status not upadated "}, status=400)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Students.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            return redirect('student-login')
        return render(request, 'auth/activate_failed.html', status=401)



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

