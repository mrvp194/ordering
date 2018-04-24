# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from models import Review, Snack, SnackManager, Inventory, InventoryManager, Category, Brand
from ..users.models import User, UserManager

# Create your views here.
def index(request): 
    if 'review' in request.session :
        request.session.pop('review')
    snacks = Snack.objects.all()
    for snack in snacks :
        snack.avg = Snack.objects.avg_rating(snack)

    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'snacks' : snacks
    }

    return render(request, 'snacks/index.html', context)

def new(request):
    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'categories' : Category.objects.all(),
        'brands' : Brand.objects.all(),
        'brand_name' : Brand.objects.all().first().name,
        'category_name' : Category.objects.all().first().name
    }
    

    return render(request, 'snacks/new.html', context)

def create(request):
    errors = Snack.objects.snack_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            request.session[tag] = error
        return redirect('/snacks/new')
    else:
        if len(request.POST['nbrand']) < 1 :
            brand = Brand.objects.filter(name=request.POST['brand'])           
        else :
            brand = Brand.objects.create(name=request.POST['nbrand'])
            brand.save()
        if len(request.POST['ncategory']) < 1 :
            category = Category.objects.filter(name=request.POST['category'])
        else :
            category = Category.objects.create(name=request.POST['ncategory'])
            category.save()
        snack = Snack.objects.create(name=request.POST['name'], price=request.POST['price'], total_purchased_amount=0, brand=brand, category=category)
        snack.save()

    return redirect('/snacks/{}'.format(Snack.objects.filter(name=snack.name)[0].id))

def review(request, id):
    if 'review' in request.session :
        request.session.pop('review')
    user = User.objects.filter(id=request.session['current_user'])[0]
    snack = Snack.objects.filter(id=id)[0]
    data = [user.id, snack.id]
    errors = Snack.objects.review_validator(data)
    if len(errors):
        for tag, error in errors.iteritems():
            request.session[tag] = error        
        return redirect('/snacks/{}'.format(snack.id))
    else :
        review = Review.objects.create(content=request.POST['content'], rating=request.POST['rating'], user=user, snack=snack)
        review.save()
        return redirect('/snacks/{}'.format(snack.id))

def show(request, id):
    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'snack' : Snack.objects.filter(id=id)[0],
        'reviews' : Snack.objects.filter(id=id)[0].review_snack.all()
    }
    

    return render(request, 'snacks/show.html', context)

def update(request, id):
        
    return redirect('/snacks/index')

def redit(request, id):
    if 'review' in request.session :
        request.session.pop('review')
    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'review' : Review.objects.filter(id=id)[0]
    }
    
    return render(request, 'snacks/edit.html', context)

def rupdate(request, id):
    if 'review' in request.session :
        request.session.pop('review')
    review = Review.objects.filter(id=id)[0]
    if len(request.POST['content']) < 1 :
        content = review.content
    else :
        content = request.POST['content']
    if 'rating' in request.POST :
        rating = request.POST['rating']
    else :
        rating = review.rating
    review.content = content
    review.rating = rating
    review.save()
    snack = review.snack
    return redirect('/snacks/{}'.format(snack.id))

def destroy(request, id):
    if 'review' in request.session :
        request.session.pop('review')
    review = Review.objects.filter(id=id)[0]
    snack = review.snack
    review.delete()
    return redirect('/snacks/{}'.format(snack.id))

def search(request):

    return render(request, 'snacks/index.html')