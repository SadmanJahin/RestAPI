from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse



def overview(request):
    
    return render(request,'index/index.html')