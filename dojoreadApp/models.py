from django.db import models
import bcrypt

class UserManager(models.Manager):
    def registerVal(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['len_name'] = "Name must contain at least 3 characters."
        if len(postData['alias']) < 3:
            errors['len_alias'] = "Alias must contain at least 3 characters."
        if len(postData['email']) < 3:
            errors['len_email'] = "Email Address must contain at least 3 characters."
        user = User.objects.filter(email = postData['email'])   #bring any data matches postData['email']
        if len(user) > 0:                                                
            register_user = user[0]
            errors['existid'] ="Email address is already exists"
        if len(postData['password']) < 3:
            errors['len_password'] = "Password must be longer than 3 characters."
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Password and Confirm PW must match."
        return errors


    def loginVal(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if len(user) > 0:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['wrongpw'] ="Password does not match"
        else:
            errors['unregistered'] = "Email addrees not registered. Try new email adress"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model): 
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name="uers_reviews", on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)