# views.py: w tym pliku znajduje się logika aplikacji. Każdy widok otrzymuje
# żądanie HTTP, przetwarza je i zwraca odpowiedź.

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

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

	# Lista aktywnych komentarzy dla danego posta.
	comments = post.comments.filter(active=True)
	# Budowę kolekcji QuerySet zaczynamy od obiektu post. Wykorzystujemy menedżera 
	# powiązanych obiektów zdefiniowanego jako comments, używając atrybutu related_name 
	# związku w modelu Comment.

	if request.method == 'POST':
		# Komentarz został opublikowany.
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Utworzenie obiektu Comment, ale jeszcze nie zapisujemy go w bazie danych.
			new_comment = comment_form.save(commit=False)
			# Przypisanie komentarza do bieżącego posta.
			new_comment.post = post
			# Zapisanie komentarza w bazie danych.
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request,
				  'blog/post/detail.html',
				  {'post': post,
				  'comments': comments,
				  'comment_form': comment_form})


def post_share(request, post_id):
	# Pobranie posta na podstawie jego identyfikatora.
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False
	to = ''

	if request.method == 'POST':
		# Formularz został wysłany.
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Weryfikacja pól formularza zakończyła się powodzeniem...
			cd = form.cleaned_data
			# ... więc można wysłać wiadomość e-mail.

			post_url = request.build_absolute_uri(post.get_absolute_url())
			# Ponieważ w wiadomości e-mail trzeba umieścić łącze do posta, bezwzględną 
			# ścieżkę dostępu posta pobieramy za pomocą metody get_absolute_url(). 
			# Następnie tej ścieżki dostępu używamy jako danych wejściowych dla metody 
			# request.build_absolute_uri() i budujemy kompletny adres URL zawierający 
			# schemat HTTP oraz nazwę hosta.

			subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], 
																	cd['email'], 
																	post.title)
			message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title, 
																									post_url, 
																									cd['name'], 
																									cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
			to = cd['to']
	else:
		form = EmailPostForm()

	return render(request, 'blog/post/share.html', {'post': post,
													'form': form,
													'to' : to,
													'sent': sent})