from django.test import TestCase

import datetime
from django.utils import timezone

from .models import Post
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

def create_user():
	"""
	テスト用のデータで使用するアカウントの作成
	"""
	user=User.objects.create_user('testuser', password='adminadmin')
	user.is_superuser=True
	user.is_staff=True
	user.save()

def create_article(user,title,text,days):
	"""
	与えられた `title''text` で質問記事を作成し、与えられた日数の `days` を 
	過去に公開された記は負の数、公開された記は正の数です。
	"""
	create = timezone.now() + datetime.timedelta(days=days-5)
	time = timezone.now() + datetime.timedelta(days=days)
	return Post.objects.create(author=user ,title=title,text=text,created_date=time, published_date=time)
	
class ArticleIndexViewTests(TestCase):
	def test_no_articles(self):
		"""
		もし記事がなければ、何も表示されない
		"""
		response = self.client.get(reverse('post_list'))
		self.assertEqual(response.status_code, 200)
		"""
		記事がない場合にhtmlがどうなっているか
		→何かしらメッセージが表示されるのか（その場合、下記メソッドの第2引数にはそのメッセージを入れる）
		"""
		self.assertContains(response, "")
		self.assertQuerysetEqual(response.context['posts'], [])
		
	def test_past_question(self):
		"""
		過去に投稿された記事を表示する
		"""
		create_user()
		me = User.objects.get(username='testuser')
		article = create_article(user=me,title="過去の記事",text="記事の内容", days=-30)
		response = self.client.get(reverse('post_list'))
		self.assertQuerysetEqual(
			response.context['posts'],
			['<Post: 過去の記事>'],
		)
	def test_future_question(self):
		"""
		pub_dateが未来の記事は表示されない
		"""
		create_user()
		me = User.objects.get(username='testuser')
		create_article(user=me,title="未来の記事",text="記事の内容", days=30)
		response = self.client.get(reverse('post_list'))
		self.assertContains(response, "")
		self.assertQuerysetEqual(response.context['posts'], [])
		
	def test_future_question_and_past_question(self):
		"""
		過去と未来の両方の質問が存在する場合でも、過去の質問だけが表示される
		
		"""
		create_user()
		me = User.objects.get(username='testuser')
		article = create_article(user=me,title="過去の記事",text="記事の内容", days=-30)
		create_article(user=me,title="未来の記事",text="記事の内容", days=30)
		response = self.client.get(reverse('post_list'))
		self.assertQuerysetEqual(
			response.context['posts'],
			['<Post: 過去の記事>'],
		)
	def test_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		"""
		create_user()
		me = User.objects.get(username='testuser')
		article1 = create_article(user=me,title="過去の記事1",text="記事の内容1", days=-30)
		article2 = create_article(user=me,title="過去の記事2",text="記事の内容2", days=-15)
		response = self.client.get(reverse('post_list'))
		self.assertQuerysetEqual(
			response.context['posts'],
			['<Post: 過去の記事1>', '<Post: 過去の記事2>'],
		)
