# Viewクラスを定義。表示するテンプレートと使用するモデルを定義
from django.shortcuts import render
from django.views.generic import ListView
from .models import Book

class ListBookView(ListView) :
    template_name = 'book/book_list.html' # テンプレートのパスを指定
    model = Book # 使用するモデルの指定
