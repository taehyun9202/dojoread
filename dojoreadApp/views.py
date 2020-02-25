from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    errors = User.objects.registerVal(request.POST)
    if len(errors) > 0:                    
        for keys, val in errors.items():  
           messages.error(request, val)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(
        name = request.POST['name'],
        alias = request.POST['alias'],
        email = request.POST['email'],
        password = pw_hash
    )
    return redirect('/books')

def login(request):
    errors = User.objects.loginVal(request.POST)
    if len(errors) > 0:                    
        for keys, val in errors.items():  
           messages.error(request, val)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['loginid'] = logged_user.id
            return  redirect('/books')

def books(request):
    if 'loginid' not in request.session:
        return redirect('/')
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        getbook = Book.objects.all()
        getreview = Review.objects.all()
        context = {
            'user': getuser,
            'reviews': getreview,
            'books': getbook
        }
    return render(request,'books.html', context)

def addbook(request):
    return render(request,'addbook.html')

def createbook(request):
    getuser = User.objects.get(id = request.session['loginid'])
    newauthor = Author.objects.create(name = request.POST['name'])
    newbook = Book.objects.create(
        title = request.POST['title'],
        author = newauthor,
        creator = getuser
    )
    newreview = Review.objects.create(
        book = newbook,
        commenter = getuser,
        content = request.POST['content'],
        rate = request.POST['rate']
    )
    return redirect(f'/books/{newbook.id}')

def bookinfo(request, bookid):
    getuser = User.objects.get(id = request.session['loginid'])
    getbook = Book.objects.get(id = bookid)
    getreview = Review.objects.filter(book = getbook)
    context ={
        'user':getuser,
        'book': getbook,
        'reviews': getreview
    }
    return render(request,'bookinfo.html',context)

def addreview(request, bookid):
    getuser = User.objects.get(id = request.session['loginid'])
    getbook = Book.objects.get(id = bookid)
    addreview = Review.objects.create(
        book = getbook,
        commenter = getuser, 
        content = request.POST['review'],
        rate = request.POST['rate']
    )
    return redirect('/books/<bookid>')

def userinfo(request, userid):
    getuser = User.objects.get(id = userid)
    getreview = Review.objects.filter(commenter = getuser)
    context = {
        'user': getuser,
        'reviews': getreview
    }
    return render(request, 'userinfo.html', context)

def deletereview(request, bookid):
    getbook = Book.objects.get(id = bookid)
    getreview = Review.objects.filter(book = getbook)
    getreview.delete()
    return redirect('/books/<bookid>')

def logout(request):    
    request.session.clear()
    return redirect('/')

