# views.py: w tym pliku znajduje się logika aplikacji. Każdy widok otrzymuje
# żądanie HTTP, przetwarza je i zwraca odpowiedź.

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	# 	Dla wyników zapytania używamy zmiennej kontekstu posts. Wartością domyślną
	# 	będzie object_list, jeśli nie zostanie podana żadna wartość context_object_name 
	paginate_by = 2
	template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug = post,
								   status = 'published',
								   publish__year = year,
								   publish__month = month,
								   publish__day = day)
	return render(request,
				  'blog/post/detail.html',
				  {'post': post})