from django.urls import path
from . import views

urlpatterns = [
	#post_listという名前のビューをルートURLに割り当て＝
	path('',views.post_list,name = 'post_list'),
	path('post/<int:pk>/',views.post_detail,name = 'post_detail'),
]
