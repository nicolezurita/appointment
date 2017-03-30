  # Inside your app's models.py file
from __future__ import unicode_literals
from django.db import models
import re, bcrypt
  # Our new manager!
  # No methods in our new manager should ever catch the whole request object
  # with a parameter!!! (just parts, like request.POST)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, postData):
        user = self.filter(email=postData['email'])
        response_to_views = {}
        if not user:
            response_to_views['status'] = False
            response_to_views['errors'] = 'email address not valid'

        else:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                response_to_views['status'] = True
                response_to_views['user'] = user[0]

            else:
                response_to_views['status'] = False
                response_to_views['errors'] = 'email/password combination not valid'

        return response_to_views

    def register(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append('Name must be at least 3 characters long!')
        if len(postData['email']) < 1:
            errors.append('Email cannot be empty!')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Enter a valid email!")
        if len(postData['password']) < 8:
            errors.append('Password must be 8 chars long!')
        if postData['password'] != postData['pwd_conf']:
            errors.append('passwords dont match!')
        if self.filter(email=postData['email']):
            errors.append('email must be unique!')

        response_to_views = {}
        if len(errors) == 0:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(name=postData['name'], email=postData['email'], password=hashed_password)
            response_to_views['user'] = user
            response_to_views['status'] = True

        else:
            response_to_views['errors'] = errors
            response_to_views['status'] = False

        return response_to_views
class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
      # *************************
      # Connect an instance of UserManager to our User model overwriting
      # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
      # *************************
