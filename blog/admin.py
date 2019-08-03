from django.contrib import admin

# admin.py: w tym pliku rejestrujemy modele, które mają być uwzględnione w witrynie
# administracyjnej Django — korzystanie z witryny administracyjnej Django jest
# opcjonalne.

# Register your models here.
from .models import Post, Comment
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish', 'status')
	# pola wyświetlane na stronie listy postów

	list_filter = ('status', 'created', 'publish', 'author')
	# Strona listy zawiera teraz prawy pasek boczny, który pozwala filtrować
    # wyniki według pól zawartych w atrybucie list_filter.

	search_fields = ('title', 'body')
    # Na stronie pojawił się pasek Search.
    # Jest to efekt zdefiniowania za pomocą atrybutu search_fields listy pól do przeszukiwania.

	prepopulated_fields = {'slug': ('title',)}
	# Poinformowaliśmy framework Django, aby wstępnie wypełnił pole slug wraz z wprowadzaniem pola title ,
	
	raw_id_fields = ('author',)
	# Ponadto teraz pole author jest wyświetlane z widżetem wyszukiwania,
    # który — gdy mamy tysiące użytkowników — skaluje się znacznie lepiej niż kontrolka rozwijanego
    # menu.
	
	date_hierarchy = 'publish'
	# Tuż pod paskiem Search znalazły się linki nawigacyjne umożliwiające poruszanie się po hierar-
    # chii dat: zdefiniowaliśmy ją za pomocą atrybutu date_hierarchy .

	ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')
