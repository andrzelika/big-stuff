from django import template
from django.db.models import Count

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
	return Post.published.count()
# Nazwę funkcji Django wykorzystuje jako nazwę znacznika. Jeżeli chcesz go zarejestrować 
# pod inną nazwą, możesz to zrobić przy użyciu atrybutu name, np. następująco:
# @register.simple_tag(name='prosty_znacznik') .

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
# Ta kolekcja QuerySet używa funkcji annotate() w celu agregacji zapytania za pomocą funkcji
# Count() . Przygotowujemy kolekcję QuerySet agregującą całkowitą liczbę komentarzy dla
# wszystkich postów w kolumnie total_comments, a następnie porządkujemy je według obliczonej
# liczby komentarzy. Ponadto dostarczana jest opcjonalna zmienna count pozwalająca na ograni-
# czenie liczby zwróconych obiektów do podanej wartości.