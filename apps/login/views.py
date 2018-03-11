from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "login/index.html")

def process(request, action):
    if action == "reg":
        validate_res = Users.objects.validate_reg(request.POST)
        if validate_res['status'] == 'bad':
            for error in validate_res['data']:
                messages.error(request, error)
            return redirect("/")
        else:
            request.session['user_id'] = validate_res['data'].id
            return redirect("/success")
    
    elif action == "log":
        login_res = Users.objects.validate_log(request.POST)
        if login_res['status'] == 'bad':
            messages.error(request, login_res['data'])
            return redirect("/")
        else:
            request.session['user_id'] = login_res['data'].id
            return redirect("/success")

def logout(request):
    request.session.flush()
    return redirect("/")

def success(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        'user' : Users.objects.get(id=request.session['user_id'])
    }
    return render(request, "login/finished.html", context)