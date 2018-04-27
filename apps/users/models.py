# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, data):
        errors = {}
        if len(data['first_name']) < 2 or any(char.isdigit() for char in data['first_name']) :
            errors['first_name'] = "Invalid First Name"
        if len(data['last_name']) < 2 or any(char.isdigit() for char in data['last_name']) :
            errors['last_name'] = "Invalid Last Name"
        if len(data['alias']) < 2 :
            errors['alias'] = "Invalid Alias"   
        if len(data['email']) < 0 or re.match(r"[^@]+@[^@]+\.[^@]+", data['email']) == None :
            errors['email'] = "Invalid Email"       
        if len(data['password']) < 8 :
            errors['password'] = "Password is too short"
        if data['password'] != data['confirmation'] :
            errors['confirmation'] = "password and confirmation aren't the same"
        if self.filter(email=data['email']).count() > 0:
            errors['email'] = "Someone with that email is already registered" 
        return errors
    def login_validator(self, data):
        errors = {} 
        if len(data['lpassword']) < 8 :
            errors['lpassword'] = "Password is too short"          
        if len(data['lemail']) < 0 or re.match(r"[^@]+@[^@]+\.[^@]+", data['lemail']) == None :
            errors['lemail'] = "Invalid Email"  
        elif self.filter(email=data['lemail']).count() == 0:
            errors['lemail'] = "You haven't registered with that email yet" 
        elif not bcrypt.checkpw(data['lpassword'].encode(), self.filter(email=data['lemail'])[0].password.encode()):
            errors['lpassword'] = "Your password doesn't match"   
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************b
    # Connect an instance of BlogManager to our Blog model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
