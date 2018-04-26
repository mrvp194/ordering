# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
import bcrypt
from models import *

# Create your views here.
def index(request) :

    return render(request, 'users/index.html')
   
def register(request) :
    if 'first_name' in request.session :
        request.session.pop('first_name')
    if 'last_name' in request.session :
        request.session.pop('last_name')
    if 'alias' in request.session :
        request.session.pop('alias')
    if 'email' in request.session :
        request.session.pop('email')
    if 'password' in request.session :
        request.session.pop('password')
    if 'confirmation' in request.session :
        request.session.pop('confirmation')
    if 'lemail' in request.session :
        request.session.pop('lemail')
    if 'lpassword' in request.session :
        request.session.pop('lpassword')
    if 'review' in request.session :
        request.session.pop('review')
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            request.session[tag] = error
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], alias=request.POST['alias'], email=request.POST['email'], password=password, is_admin=False)
        user.save()
        request.session['current_user'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/snacks')

def login(request) :
    if 'first_name' in request.session :
        request.session.pop('first_name')
    if 'last_name' in request.session :
        request.session.pop('last_name')
    if 'alias' in request.session :
        request.session.pop('alias')
    if 'email' in request.session :
        request.session.pop('email')
    if 'password' in request.session :
        request.session.pop('password')
    if 'confirmation' in request.session :
        request.session.pop('confirmation')
    if 'lemail' in request.session :
        request.session.pop('lemail')
    if 'lpassword' in request.session :
        request.session.pop('lpassword')
    if 'review' in request.session :
        request.session.pop('review')
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            request.session[tag] = error
        return redirect('/')
    else:
        request.session['current_user'] =  User.objects.filter(email=request.POST['lemail'])[0].id
        return redirect('/snacks')

def show(request, id):
    count = len(User.objects.filter(id=id)[0].review_user.all())
    context = {
        'user' : User.objects.filter(id=id)[0],
        'count' : count
    }
    return render(request, 'users/show.html', context)

def update(request, id):

    return redirect('users/show')

def logout(request):
    request.session.clear()
    return render(request, 'users/index.html')