from django.db import models

# https://docs.djangoproject.com/ja/5.1/topics/db/models/
CATEGORY = (('business', 'ビジネス'), ('life', '生活'), ('other', 'その他'))

class Book(models.Model):
    title = models.CharField(max_length=100) # titleという名前のCharField(文字列型)のテーブルを定義。
    text = models.TextField(max_length=255)
    category = models.TextField(
        max_length=100,
        choices= CATEGORY # choicesオプション https://arc.net/l/quote/lehwmztf
    )

    def __str__(self): # 管理画面でオブジェクトをtitleの文字列で表示する
      return self.title
