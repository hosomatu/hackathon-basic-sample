# ルーティング設定のファイル
# ここはプロジェクトのurls.pyなので、ここからアプリのurls.pyを呼び出す設定が必要。
"""hackathonbasic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# プロジェクトが受け取るHTTPリクエストに対するリストを定義。
# path()関数。第一引数がurlパス。第二引数がビュー関数など、マッチしたら呼び出されるもの。
# include()関数。他のアプリケーションのURL設定をプロジェクト全体のURL設定に組み込むために使用させるメソッド。
# pathもincludeもdjango.urlsモジュールに定義されているただの関数。メソッドではない。
# https://docs.djangoproject.com/ja/5.1/ref/urls/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), #認証機能appをこのプロジェクトに追加
    path('', include('book.urls')), # book/urls.py内で定義されたパスがこのプロジェクトに追加される。
]
