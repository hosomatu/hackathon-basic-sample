from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . views import SignupView

app_name = 'accounts' #ここでapp_nameを定義することで、テンプレートにて href = "{% url 'accounts:login %}" のような使い方ができる

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), #LoginViewを呼び出せば、特段指定しなくても、root/templates/registration/login.htmlを呼び出してくれる。 https://docs.djangoproject.com/ja/5.1/topics/auth/default/#django.contrib.auth.views.LoginView
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
