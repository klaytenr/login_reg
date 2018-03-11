from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Model Managers

class UsersManager(models.Manager):
    def validate_reg(self, postData):
        errors = []
        res = {
            "status" : "good",
            "data" : ""
        }
        #first and last name
        if len(postData["first_name"]) < 2 or len(postData["last_name"]) < 2:
            errors.append("First and Last name must be at least 2 characters long.")
        if not postData["first_name"].isalpha() or not postData["last_name"].isalpha():
            errors.append("First and Last name must be letters only.")
        #email
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be in proper format.")
        #password
        if len(postData["password"]) < 8:
            errors.append("Password must be at least 8 characters long.")
        if postData["password"] != postData["password_conf"]:
            errors.append("Password must match confirmation.")        
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            hash1=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = Users.objects.create(first_name=postData["first_name"], last_name=postData["last_name"], email=postData["email"], password=hash1)
            res['data'] = user
        return res
    
    def validate_log(self, postData):
        res = {
            'status' : 'good',
            'data' : ""
        }
        try:
            the_user = Users.objects.get(email=postData['email'])
        except:
            res['status'] = 'bad'
            res['data'] = "Email or Password incorrect"
            return res
        if bcrypt.checkpw(postData['password'].encode(), the_user.password.encode()):
            res['data'] = the_user
            return res
        else:
            res['status'] = 'bad'
            res['data'] = "Email or Password incorrect"
            return res


# Create your models here

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

    def __str__(self):
        return "<User: {}>".format(self.email)