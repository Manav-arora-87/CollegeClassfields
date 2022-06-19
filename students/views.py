from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
import bcrypt
from math import ceil
from students.models import Students,Products

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.files.storage import default_storage
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
from django.contrib.auth.decorators import login_required
import uuid , os , json,requests
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
    return render(request,'index.html')

def CheckStudentLogin(request):
    

    try:
        request.session['student']=admin.id
        print("Manav")
        emailid = request.POST['emailid']
        print("email id " , emailid)
        password = request.POST['password']
        admin=Students.objects.get(emailid=emailid)
        #recaptcha stuff 
        clientkey = request.POST['g-recaptcha-response']
        secretkey = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        captchadata={'secret':secretkey,'response':clientkey}
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        print(verify)
        # # Adminlogins.ob
        if bcrypt.checkpw(password.encode("utf8"), admin.password.encode("utf8")) and verify:
             request.session['student']=admin.id
             return redirect('student-dashboard')
        else:
            return render(request, "login.html",{'msg': 'Please enter correct password or tick the recaptcha'})
        

    except Exception as e:
          print(e)  
          Logout(request) 
          return render(request, "login.html", {'msg': 'Please enter correct password or tick the recaptcha'})

def Studentdashboard(request):
    
    try:
        
        result = request.session['student']
        products=reversed(Products.objects.all())
        temp=Products.objects.all()

        return render(request, "Dashboard.html",{'products':products,'temp':temp})

    
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
        category=request.POST['category']
        description = request.POST['desc']
        price = request.POST['price']
        productage = request.POST['productage']
        img = request.FILES['productimg']
        t=Products.objects.create(img=img,productname=name,category=category,productdesc=description,price=price,productage=productage,studentid_id=result)
        t.save()
        return redirect('student-buysell')


    
    except  Exception as e:
        print("Product_Submit",e)
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
    mobno= request.POST['mobno']
    branch= request.POST['branch']
    year= request.POST['year']
    address= request.POST['address']
    
    salt= bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd.encode("utf8"),salt)
    hashed=(hashed.decode("utf8"))
    t=Students.objects.create(mob=mobno,emailid=clgemail,is_active=0,password=hashed,name=name,branch=branch,address=address,year=year) #clgid needs to be removed
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


def searchMatch(query, item):
    if query in item.productdesc.lower() or query in item.productname.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    
    for cat in cats:
        prodtemp = Products.objects.filter(category=cat)
        for item in prodtemp :
           if searchMatch(query, item):
               prod=item
               allProds.append(prod)
       
    
    return render(request, 'search.html', {'products':allProds})