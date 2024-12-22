from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm) :
    class Meta : # フォームやモデルに関連する設定情報をまとめる特別なクラス。受け取った情報をどこのモデルで保存するのかと、ブラウザ上に表示する項目を指定
        model = User # Djangoがデフォルトで用意しているモデル
        fields = { 'username' }