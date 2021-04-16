from django.db import models
import re
import bcrypt

# Create your models here.
class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = ("Invalid email address!")
        if check:
            errors['email'] = "Email has already been registered."
        if len(postData['firstname']) < 2:
            errors['firstname'] = "First Name should be at least 2 charachters"
        if len(postData['lastname']) < 2:
            errors['lastname'] = "Last Name should be at least 2 charachters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match!'
        return errors
    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['pw'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors


class User(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()
    def save(self, *args, **kwargs):
         super(User, self).save(*args, **kwargs)

class DateManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must consist of at least 3 characters!"
        if len(postData['description']) < 10:
            errors['description'] = "The description must be at least 10 characters!"
        if len(postData['location']) < 1:
            errors['location'] = "Location is required!"
        return errors
    def edit_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must consist of at least 3 characters!"
        if len(postData['description']) < 10:
            errors['description'] = "The description must be at least 10 characters!"
        if len(postData['location']) < 1:
            errors['location'] = "Location is required!"
        return errors

class Date(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    cost = models.CharField(max_length=5)
    liked_by = models.ManyToManyField(User, related_name="users_who_like")
    completed_by = models.ManyToManyField(User, related_name="users_who_complete")
    uploaded_by = models.ForeignKey(User, related_name = 'user_who_uploaded', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DateManager()
