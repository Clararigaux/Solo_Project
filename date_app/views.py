from django.shortcuts import render, redirect
from .models import User, Date
from django.contrib import messages
import bcrypt
from datetime import datetime
from django.urls import reverse

# Create your views here.
def register_page(request):
    return render(request, 'register.html')

def register(request):   
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
        new = User.objects.create(firstname=request.POST['firstname'], lastname=request.POST['lastname'], email=request.POST['email'], password=pw_hash)
        request.session['user'] = new.firstname
        request.session['id'] = new.id
        return redirect("../success/") 

def login(request):
    return render(request, 'login.html')

def validate_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user'] = user.firstname
        request.session['id'] = user.id
        return redirect('../success/')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "dates": Date.objects.all(),
        "user": user,
        "users": User.objects.all()
    }
    return render(request, 'success.html', context)


def add_date(request):
    return render(request, 'add_date.html')

def create(request):
    errors = Date.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('../add_date/')
    else:
        this_date = Date.objects.create(
            name=request.POST['name'], 
            description=request.POST['description'], 
            location=request.POST['location'],
            cost=request.POST['cost'],
            uploaded_by=User.objects.get(id=(int(request.session['id'])))
            )
        request.session['name_id'] = this_date.id
        return redirect("../success/")  

def delete(request, date_id):
    to_delete = Date.objects.get(id=date_id)
    to_delete.delete()
    return redirect('../../success/')

def edit(request, date_id):
    date = Date.objects.get(id=date_id)
    user = User.objects.get(id=(int(request.session['id'])))
    context = {
        "date": Date.objects.get(id=date_id),  
    }
    return render(request, 'update.html', context)

def update(request, date_id):
    errors = Date.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('edit', date_id=date_id)
    else:
        date = Date.objects.get(id=date_id)
        date.name = request.POST['name']
        date.description = request.POST['description']
        date.cost = request.POST['cost']
        date.save()
    return redirect("../../../success/")

def view(request, date_id):
    user = User.objects.get(id=(int(request.session['id'])))
    context = {
        "date": Date.objects.get(id=date_id),
        "user": user
    }
    return render(request, 'view.html', context)

def complete(request, date_id):
    this_date = Date.objects.get(id=date_id)
    user = User.objects.get(id=(int(request.session['id'])))
    user.users_who_complete.add(this_date)
    user.save()
    return redirect('../../success/')

def favorite(request, date_id):
    this_date = Date.objects.get(id=date_id)
    user = User.objects.get(id=(int(request.session['id'])))
    user.users_who_like.add(this_date)
    user.save()
    return redirect('../../success/')

def unfavorite(request, date_id):
    this_date = Date.objects.get(id=date_id)
    user = User.objects.get(id=(int(request.session['id'])))
    user.users_who_like.remove(this_date)
    user.save()
    return redirect('../../success/')