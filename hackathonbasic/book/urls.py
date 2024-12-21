# プロジェクト全体のurls.pyから指定されているファイル。
from django.urls import path
from . import views

# path()関数。第一引数がurlパス。第二引数がビュー関数など、マッチしたら呼び出されるもの。第3引数はURLに名前をつけている。
urlpatterns = [
    path('book/', views.ListBookView.as_view(), name='list-book'), #class-based viewの書き方
    path('', views.index_view, name='index'), #function-based viewの書き方
    path('book/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'), #整数型のプライマリーキー(id)
    path('book/create/', views.CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>/delete', views.DeleteBookView.as_view(), name='delete-book'),
    path('book/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
]