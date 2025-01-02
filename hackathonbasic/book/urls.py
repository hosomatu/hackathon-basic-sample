# プロジェクト全体のurls.pyから指定されているファイル。
from django.urls import path
from . import views

# path()関数。第一引数がurlパス。第二引数がビュー関数など、マッチしたら呼び出されるもの。第3引数はURLに名前(viewでhref="{% url 'list-book %}"的な感じで使える)をつけている。
urlpatterns = [
    path('book/', views.ListBookView.as_view(), name='list-book'), #class-based viewの書き方。ListBookViewクラスを呼び出す。views.pyに定義されている。
    path('', views.index_view, name='index'), #function-based viewの書き方。index_view関数を呼び出す。views.pyに記載されている。
    path('book/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'), #整数型のプライマリーキー(id)。Djnagoのpath関数ではurlのintをキャプチャして、pkという名前の変数としてViewに渡すことができる。クラスベースビューの場合はpkは自動的に対象モデルのプライマリーキーとして解釈される。
    path('book/create/', views.CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>/delete', views.DeleteBookView.as_view(), name='delete-book'),
    path('book/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
    path('book/<int:book_id>/review/', views.CreateReview.as_view(), name='review'), # ここのpk変数は、get_success_urlメソッドで使用されている
]