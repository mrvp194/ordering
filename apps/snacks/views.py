# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from operator import itemgetter
from models import Review, Snack, SnackManager, Category, Brand
from ..users.models import User, UserManager
import requests
import datetime
import openfoodfacts
from django.utils import timezone
# Create your views here.
def index(request): 
    if 'review' in request.session :
        request.session.pop('review')
    snacks = Snack.objects.all().order_by('name')
    for snack in snacks :
        snack.avg = Snack.objects.avg_rating(snack)

    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'snacks' : snacks
    }

    return render(request, 'snacks/index.html', context)

def new(request, id):
    context = {
            'user' : User.objects.filter(id=request.session['current_user'])[0],
            'categories' : Category.objects.all(),
            'brands' : Brand.objects.all()
        }
    if id == None :
        context['snack'] = {}
        
    else :
        search_result = openfoodfacts.products.get_product(id)
        snack = {}
        snack['search'] = ''
        snack['id'] = search_result['product']['code']
        snack['name'] =  search_result['product']['product_name']
        if ' brands' in search_result['product'] :
            snack['brand'] = search_result['product']['brands']
        snack['picture_url'] =  search_result['product']['image_front_url']
        context['snack'] = snack
    

    return render(request, 'snacks/new.html', context)

def create(request):
    errors = Snack.objects.snack_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            request.session[tag] = error
        return redirect('/snacks/new')
    else:
        if len(request.POST['nbrand']) < 1 :
            brand = Brand.objects.filter(name=request.POST['brand'])[0]         
        else :
            brand = Brand.objects.create(name=request.POST['nbrand'])
            brand.save()
        if len(request.POST['ncategory']) < 1 :
            category = Category.objects.filter(name=request.POST['category'])[0]
        else :
            category = Category.objects.create(name=request.POST['ncategory'])
            category.save()
        snack = Snack.objects.create(name=request.POST['name'], picture_url=request.POST['picture_url'], price=0, total_purchased_amount=0, brand=brand, category=category, quantity=0)
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
    snack = Snack.objects.filter(id=id)[0]
    snack.avg = Snack.objects.avg_rating(snack)
    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'snack' : snack,
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
    review.updated_at = timezone.now()
    review.save()
    snack = review.snack
    return redirect('/snacks/{}'.format(snack.id))

def cart(request):
    # request.session.pop('cart')
    if 'cart' not in request.session :
        request.session['cart'] = {}
    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'cart' : request.session['cart']
    }
    # print request.session['cart']
    return render(request, 'snacks/cart.html', context)

def add(request, id):
    if 'cart' not in request.session :
        request.session['cart'] = {}
    snack = Snack.objects.filter(id=id)[0]
    cart = request.session['cart']
    # request.session.pop('cart')
    formatted_snack = {
                        'id' : snack.id,
                        'name' : snack.name,
                        'total_purchased_amount' : snack.total_purchased_amount,
                        'brand' : snack.brand.name,
                        'picture_url' : snack.picture_url,
                        'category' : snack.category.name,
                        'quantity' : snack.quantity,
                        'avg' : Snack.objects.avg_rating(snack)
                    }

    cart[formatted_snack['id']] = formatted_snack
    request.session['cart'] = cart
    request.session.modified = True
    print request.session['cart']
    # context = {
    #     'user' : User.objects.filter(id=request.session['current_user'])[0],
    #     'cart' : request.session['cart']
    # }
    return redirect('/snacks/')

# def checkout(request) :


def destroy(request, id):
    if 'review' in request.session :
        request.session.pop('review')
    review = Review.objects.filter(id=id)[0]
    snack = review.snack
    review.delete()
    return redirect('/snacks/{}'.format(snack.id))

def search(request):
    search_result = openfoodfacts.products.advanced_search({
                                                            "search_terms":request.POST['search']
                                                        })
    # search_result = openfoodfacts.products.search(request.POST['search'], 1, 20, 'unique_scans','united states')
    # print search_result['products']
    snacks = []
    for val in search_result['products']:
        if 'image_front_url' in val :
            if not len(val['image_front_url']) == 0:
                if val['product_name'] == 'Full on flavour - Four cheese & red onion':
                    print val['image_front_url']
                snack = {}
                snack['search'] = ''
                snack['id'] = val['code']
                snack['name'] =  val['product_name']
                if ' brands' in val :
                    snack['brand'] = val['brands']
                snack['picture_url'] =  val['image_front_url']
                snacks.append(snack)
    our_snacks = Snack.objects.filter(name__contains='{}'.format(request.POST['search']))
    for snack in our_snacks :
        snack.avg = Snack.objects.avg_rating(snack)
        snacks.append(snack)
    context = {
        'user' : User.objects.filter(id=request.session['current_user'])[0],
        'snacks' : snacks
    }
    return render(request, 'snacks/search.html', context)

def destroysnack(request, id):
    if str(id) in request.session['cart'] :
        del request.session['cart'][str(id)]
        request.session.modified = True
    return redirect('/snacks/cart')

def newlyadded(request):

    context = {
    'snacks': Snack.objects.all().order_by('created_at'),
    'user' : User.objects.filter(id=request.session['current_user'])[0]
    }

    return render(request, 'snacks/index.html', context)

def top(request):

    snacks = Snack.objects.all()
    s = []
    for snack in snacks :
        formatted_snack = {
            'id' : snack.id,
            'name' : snack.name,
            'price' : snack.price,
            'total_purchased_amount' : snack.total_purchased_amount,
            'picture_url' : snack.picture_url,
            'brand' : snack.brand,
            'category' : snack.category,
            'created_at' : snack.created_at,
            'quantity' : snack.quantity,
            'avg' : Snack.objects.avg_rating(snack)
        }
        s.append(formatted_snack)
        s = sorted(s, key=itemgetter('avg'))
        s.reverse()

    context ={
    'snacks': s,
    'user' : User.objects.filter(id=request.session['current_user'])[0]
    }

    return render(request, 'snacks/index.html', context)


def mostreviewed(request):

    snacks = Snack.objects.all()
    s = []
    for snack in snacks :
        formatted_snack = {
            'id' : snack.id,
            'name' : snack.name,
            'price' : snack.price,
            'total_purchased_amount' : snack.total_purchased_amount,
            'picture_url' : snack.picture_url,
            'brand' : snack.brand,
            'category' : snack.category,
            'created_at' : snack.created_at,
            'quantity' : snack.quantity,
            'avg' : Snack.objects.avg_rating(snack),
            'count' : snack.review_snack.count()
        }
        s.append(formatted_snack)
        s = sorted(s, key=itemgetter('count'))
        s.reverse()


    context ={
    'snacks': s,
    'user' : User.objects.filter(id=request.session['current_user'])[0]
    }


    return render(request, 'snacks/index.html', context)

def quantity(request, id):
    snack = Snack.objects.filter(id=id)[0]
    if str(id) in request.session['cart'] :
        request.session['cart'][str(id)]['quantity'] = request.POST['quantity']
        request.session.modified = True
        snack.quantity = request.POST['quantity']
        snack.save()
        return redirect('/snacks/cart')
    else :
        snack.quantity = request.POST['quantity']
        snack.save()

        return redirect('/snacks/inventory')


def checkout(request):
    cart = request.session['cart']
    for snack in cart :
        s = Snack.objects.filter(id=snack)[0]
        quantity = request.session['cart'][snack]['quantity']
        s.total_purchased_amount += int(quantity)
        s.save()
    request.session['cart'].clear()
    request.session.modified = True
    
    
    return redirect('/snacks/inventory')

def inventory(request):
    snacks = Snack.objects.filter(quantity__gt=0)
    context =  {
        'snacks' : snacks,
        'user' : User.objects.filter(id=request.session['current_user'])[0]
    }
    return render(request, 'snacks/inventory.html', context)