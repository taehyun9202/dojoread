from django.urls import path
from .import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('logout', views.logout),
    path('books/add', views.addbook),
    path('books/create',views.createbook),
    path('books/<bookid>', views.bookinfo),
    path('books/<bookid>/addreview', views.addreview),
    path('books/<bookid>/delete', views.deletereview),
    path('users/<userid>', views.userinfo)
    
]
