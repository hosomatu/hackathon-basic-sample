# adminで該当のテーブルを確認するためにmodelを登録する必要がある。
from django.contrib import admin
from .models import Book

admin.site.register(Book)