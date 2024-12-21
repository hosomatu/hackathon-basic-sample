# プロジェクト全体のurls.pyから指定されているファイル。
from django.urls import path
from . import views

# path()関数。第一引数がurlパス。第二引数がビュー関数など、マッチしたら呼び出されるもの。
urlpatterns = [
    path('book/', views.ListBookView.as_view()),
    path('book/<int:pk>/detail/', views.DetailBookView.as_view()), #プライマリーキー(id)
]