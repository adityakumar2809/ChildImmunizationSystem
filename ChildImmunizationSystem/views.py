from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def fault(request, msg):
    return render(request, 'fault.html', {'msg': msg})