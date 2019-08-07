# Utworzenie pliku urls.py dla każdej aplikacji jest najlepszym sposobem zapewnienia możliwości wielokrot-
# nego użycia tej aplikacji w innych projektach.

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	# Widoki posta
	path('', 
		 views.post_list, 
		 name = 'post_list'),
	# path('', views.PostListView.as_view(), name='post_list'),
	path('tag/<slug:tag_slug>/',
		 views.post_list, 
		 name='post_list_by_tag'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
		  views.post_detail,
		  name = 'post_detail'),
	path('<int:post_id>/share/', 
		 views.post_share, 
		 name='post_share'),
]


# Do przechwytywania wartości z adresu URL używamy nawiasów trójkątnych. Każda wartość
# określona we wzorcu adresu URL jako <parametr> jest przechwytywana jako ciąg znaków.
# Używamy konwerterów ścieżek, np. <int: year> , aby dokładnie dopasować i zwrócić liczbę
# całkowitą, oraz <slug: post> , by dokładnie dopasować do slugu (ciąg składający się z liter lub
# cyfr ASCII oraz znaków łącznika i podkreślenia). Z wszystkimi konwerterami ścieżek dostarczo-
# nymi z frameworkiem Django można zapoznać się na stronie https://docs.djangoproject.
# com/en/2.0/topics/http/urls/#path-converters.