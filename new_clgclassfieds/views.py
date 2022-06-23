from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from students.models import *
from datetime import *

# Create your views here.
def HOME(request):
    res=Students.objects.all()
    print(res)
    return render(request,'index.html')
