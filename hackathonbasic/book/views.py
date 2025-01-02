# Viewクラスを定義。表示するテンプレートと使用するモデルを定義
# railsでいうコントローラー
# urls.pyのpathメソッドの第二引数で指定されて、それぞれのクラスや関数が呼び出される

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin # DjangoのMixinは、Djangoのクラスベースビュー（CBV）やモデルでコードの再利用性を高めるための設計パターン
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE #const.pyにて定めた定数

class ListBookView(LoginRequiredMixin, ListView) : #Pythonでは()の部分が継承する親クラス。LoginRequiredMixinによってログインしていない状態では表示しないようになる。ログインしていない場合はデフォルトでaccounts/loginに飛ばされる(settings.pyのLOGIN_URLで調整可能)
    template_name = 'book/book_list.html' # テンプレートのパスを指定
    model = Book # 使用するモデルの指定
    paginate_by = ITEM_PER_PAGE # class-based view の場合は簡単にページネーションを実装できる。関数ベースだと結構めんどい(下)

class DetailBookView(LoginRequiredMixin, DetailView) :
    template_name = 'book/book_detail.html'
    model = Book

class CreateBookView(LoginRequiredMixin, CreateView) :
    template_name = 'book/book_create.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail') # フォームの内容
    success_url = reverse_lazy('list-book') # reverce逆の動作。つまり普段はurlからviewsの名前を得ているがそれの逆(viewの名前からurlを得る)を行う。lazyによりDjangoの初期化のタイミングで処理が走らないように送らせている。

class DeleteBookView(LoginRequiredMixin, DeleteView) :
    template_name = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None) :
        obj = super().get_object(queryset) #親クラスのget_objectメソッドでBookインスタンスを取得。queryset はデータベースから取得するデータの集合。urlに対応したオブジェクトをとってくる。

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj

class UpdateBookView(LoginRequiredMixin, UpdateView) :
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')
    template_name = 'book/book_update.html'
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None) :
        obj = super().get_object(queryset) #親クラスのget_objectメソッドでBookインスタンスを取得。queryset はデータベースから取得するデータの集合。urlに対応したオブジェクトをとってくる。

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj
    
    def get_success_url(self) : # 親クラスのUpdateViewにあるget_success_urlメソッドをオーバーライド。pythonの引数selfは、現在のビューのインスタンス。つまりUpdateBookViewのインスタンス
        return reverse('detail-book', kwargs={'pk': self.object.id}) # reverseによって、URLの名前からURLを生成する。pkというプレースホルダーにこのインスタンスのobjectのidを格納。urls.pyのdetail-bookのパスでpkというプレースホルダーがある部分で使われる。

def index_view(request) :
    # テンプレートの中で使用する変数
    object_list = Book.objects.order_by('-id')
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating') # annotateはクエリセット(DBからもらえるオブジェクト)に別の計算結果を追加するメソッド。reviewモデルのrateフィールド

    paginator = Paginator(ranking_list, ITEM_PER_PAGE) # Djangoが用意しているPaginatorクラスからオブジェクトを作成。関数ベースだと大変
    page_number = request.GET.get('page', 1) # http://example.com/books/?page=3 のときは3を返す。pageに何もなかったら1が帰る
    page_obj = paginator.page(page_number) #つまり、ランキングリスト全体を分割してオブジェクトとしている

    # renderメソッド。テンプレートをレンダリングしてレスポンスオブジェクトを作る関数。
    # 第一引数のrequestは現在のリクエストオブジェクトを指定。第二引数でテンプレートファイルを指定。
    # 第三引数でテンプレートに渡すコンテキスト（辞書形式のデータ)先に定義したobject_list(右)を'object_list'(左)という名前で呼び出せるようにしている
    return render(
        request,
        'book/index.html',
        {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj': page_obj} # コンテキスト(辞書型でテンプレートに対して渡すやつ)として変数を渡している。
        )

class CreateReview(LoginRequiredMixin, CreateView) :
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'book/review_form.html'

    def get_context_data(self, **kwargs) : #元々CreateViewにあるget_context_dataメソッドを上書き。**kwargsはPythonの関数定義において可変長キーワード引数を表す。今回は<int:book_id>が入る。
        context = super().get_context_data(**kwargs) #contextは辞書型のデータでrenderメソッドの3つ目の引数のやつ。superで親クラスCreateViewのget_context_dataを呼び出して返り値を格納。
        context['book'] = Book.objects.get(pk=self.kwargs['book_id']) #辞書型のcotextにbookを格納している。bookとは右側の部分。
        return context #これでReviewのcontexxtにurlのidに該当する本の内容を渡すことができるようになった。
    
    def form_valid(self, form) : # CreateViewのメソッドを上書き
        form.instance.user = self.request.user # formクラスのインスタンスにuserというデータを追加している。その内容は右側。ログインしている場合のrequestオブジェクトに入っているuser情報。

        return super().form_valid(form)
    
    def get_success_url(self) :
        return reverse('detail-book', kwargs={'pk': self.object.book.id}) # detail-bookはtemplateの名前。キーワード引数に書籍のidを私ている