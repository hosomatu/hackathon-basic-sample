# Viewクラスを定義。表示するテンプレートと使用するモデルを定義
# railsでいうコントローラー

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Book

class ListBookView(ListView) : #Pythonでは()の部分が継承する親クラス
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

class DeleteBookView(DeleteView) :
    template_name = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

class UpdateBookView(UpdateView) :
    model = Book
    fields = ('title', 'text', 'category' )
    template_name = 'book/book_update.html'
    success_url = reverse_lazy('list-book')

def index_view(request) :
    object_list = Book.objects.order_by('category')

    # renderメソッド。テンプレートをレンダリングしてレスポンスオブジェクトを作る関数。
    # 第一引数のrequestは現在のリクエストオブジェクトを指定。第二引数でテンプレートファイルを指定。
    # 第三引数でテンプレートに渡すコンテキスト（辞書形式のデータ)先に定義したobject_list(右)を'object_list'(左)という名前で呼び出せるようにしている
    return render(request, 'book/index.html', {'object_list': object_list})