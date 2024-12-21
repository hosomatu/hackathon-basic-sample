# Viewクラスを定義。表示するテンプレートと使用するモデルを定義
# railsでいうコントローラー

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Book

class ListBookView(ListView) :
    template_name = 'book/book_list.html' # テンプレートのパスを指定
    model = Book # 使用するモデルの指定

class DetailBookView(DetailView) :
    template_name = 'book/book_detail.html'
    model = Book

class CreateBookView(CreateView) :
    template_name = 'book/book_create.html'
    model = Book
    fields = ('title', 'text', 'category')
    success_url = reverse_lazy('list-book') # reverce逆の動作。つまり普段はurlからviewsの名前を得ているがそれの逆(viewの名前からurlを得る)を行う。lazyによりDjangoの初期化のタイミングで処理が走らないように送らせている。