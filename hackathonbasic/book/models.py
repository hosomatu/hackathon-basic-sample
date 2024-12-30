from django.db import models
from . consts import MAX_RATE

# https://docs.djangoproject.com/ja/5.1/topics/db/models/
CATEGORY = (('business', 'ビジネス'), ('life', '生活'), ('other', 'その他'))
RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)] # [(0,'0'),(1,'1'),(2,'2'),,,]のようなデータを返す

class Book(models.Model):
    title = models.CharField(max_length=100) # titleという名前のCharField(文字列型)のテーブルを定義。
    text = models.TextField(max_length=255)
    category = models.TextField(
        max_length=100,
        choices= CATEGORY # choicesオプション https://arc.net/l/quote/lehwmztf
    )

    def __str__(self): # 管理画面でオブジェクトをtitleの文字列で表示する
        return self.title

class Review(models.Model) :
    book = models.ForeignKey(Book, on_delete=models.CASCADE) #外部キーにBookを定義。ondeleteでBookが削除されたらReviewも削除される
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)