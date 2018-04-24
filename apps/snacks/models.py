# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User
from django import template


# Create your models here.
# class ReviewManager(models.Manager):

class SnackManager(models.Manager):
    def snack_validator(self, data):
        errors = {}
        if len(data['name']) < 2 :
            errors['name'] = "That's not a snack name"
        if 'nbrand' in data :
            if data['nbrand'] < 1 :
                errors['nbrand'] = 'Not a valid brand'
        else :
            if len(data['brand']) < 1 :
                errors['brand'] = "That's not a valid brand"
        if 'ncategory' in data :
            if data['ncategory'] < 1 :
                errors['ncategory'] = 'Not a valid category'
        else :
            if len(data['category']) < 1 :
                errors['category'] = "That's not a valid category"
        if data['price'] <= 0.00 :
            errors['price'] = "That's not a valid price"
        return errors

    def avg_rating(self, snack) :
        reviews = snack.review_snack.all()
        total = 0
        for review in reviews :
            total += review.rating
        if len(reviews) == 0 :
            length = 1
        else :
            length = len(reviews)
        return total/length 

    def review_validator(self, data):
        errors = {}
        user = User.objects.filter(id=data[0])[0]
        snack = Snack.objects.filter(id=data[1])[0]
        if len(Review.objects.filter(user=user, snack=snack)) > 0:
            errors['review'] = 'You already reviewed this snack!'
        return errors

class InventoryManager(models.Manager):
    def inventory_validator(self, data):
        errors = {}
        if data['quantity'] < 1 :
            errors['quantity'] = "Not a valid quantity"
        if len(data['snack']) < 1 :
            errors['snack'] = "That's not a snack"
        return errors


class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # objects = BrandManager()

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # objects = CategoryManager()

class Snack(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    total_purchased_amount = models.IntegerField()
    brand = models.ForeignKey(Brand, related_name='brand')
    # picture_url = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='category')
    created_at = models.DateTimeField(auto_now_add=True)
    avg = 0
    objects = SnackManager()

class Inventory(models.Model):
    quantity = models.IntegerField()
    snack = models.ForeignKey(Snack, related_name='inventory_snack')
    created_at = models.DateTimeField(auto_now_add=True)
    # ohbjects = InventoryManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name='user')
    snack = models.ForeignKey(Snack, related_name='review_snack')
    created_at = models.DateTimeField(auto_now_add=True)
    # objects = ReviewManager()

# @register.simple_tag
