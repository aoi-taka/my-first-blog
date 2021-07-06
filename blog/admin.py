from django.contrib import admin
from .models import Post

#作成したPostモデルを管理画面(adminページ)上で見えるようにする
admin.site.register(Post)

