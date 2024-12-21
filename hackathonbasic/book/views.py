# Viewクラスを定義。表示するテンプレートと使用するモデルを定義
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book

class ListBookView(ListView) :
    template_name = 'book/book_list.html' # テンプレートのパスを指定
    model = Book # 使用するモデルの指定

class DetailBookView(DetailView) :
    template_name = 'book/book_detail.html'
    model = Book