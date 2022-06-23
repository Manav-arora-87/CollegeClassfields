from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect

from datetime import *

# Create your views here.
def HOME(request):
    return render(request,'index.html')
