# models.py: modele danych aplikacji — plik models.py musi znajdować się we
# wszystkich aplikacjach Django, choć może pozostać pusty.

# Model
# to klasa Pythona, która jest podklasą klasy django.db.models.Model . Każdy atrybut tej klasy 
# reprezentuje pole bazy danych. Django tworzy tabelę dla każdego modelu zdefiniowanego w pliku
# models.py. Kiedy definiujesz model, Django udostępnia praktyczny interfejs API do łatwego
# odpytywania obiektów w bazie danych.


# Wszystkie typy pól 
# można znaleźć pod adresem https://docs.djangoproject.com/en/2.0/ref/models/fields/.



from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
   def get_queryset(self):
       return super(PublishedManager,
                   self).get_queryset().filter(status='published')
# Własny manager do QuerySetów klasy Post zwracający tylko opublikowane posty


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)

	title = models.CharField(max_length = 250)
# 	title : pole reprezentujące tytuł posta. Jest to pole typu CharField , co odpowiada 
# 	kolumnie VARCHAR w bazie danych SQL.

	slug = models.SlugField(max_length = 250,
							unique_for_date = 'publish')
# 	slug : pole przeznaczone do użycia w adresach URL. Jest to krótka etykieta
# 	zawierająca wyłącznie litery, cyfry, znaki podkreślenia lub łączniki. Pola slug
# 	będziemy używać do tworzenia opisowych, przyjaznych dla SEO (ang. Search
# 	Engine Optimization) adresów URL postów na blogu. Dodaliśmy do tego pola
# 	parametr unique_for_date , aby budować adresy URL postów z wykorzystaniem
# 	daty publikacji i pola slug . Django nie dopuści do tego, aby więcej niż jeden post
# 	miał taką samą wartość pola slug dla danej daty.
	
	author = models.ForeignKey(User,
							   on_delete = models.CASCADE,
							   related_name = 'blog_posts')
# 	author : to pole jest kluczem obcym. Definiuje relację wiele do jednego. Informujemy
# 	Django o tym, że każdy post jest napisany przez określonego użytkownika. Natomiast
#	użytkownik może napisać dowolną liczbę postów. Za pomocą tego pola Django
# 	utworzy klucz obcy w bazie danych z wykorzystaniem klucza głównego powiązanego
# 	modelu. W tym przypadku bazujemy na modelu User systemu uwierzytelniania
# 	Django. Parametr on_delete określa zachowanie podczas usuwania obiektu. Nie jest
# 	ono specyficzne dla Django. Jest to zgodne ze standardem SQL. Jeśli wprowadzimy
# 	słowo kluczowe CASCADE , określamy, że po usunięciu użytkownika z bazy danych
# 	zostaną usunięte również powiązane z nim posty na blogu. Wszystkie możliwe
# 	opcje można znaleźć pod adresem https://docs.djangoproject.com/en/2.0/ref/models/
# 	fields/#django.db.models.ForeignKey.on_delete. Za pomocą atrybutu related_name
# 	podajemy nazwę odwróconej relacji — od User do Post . To pozwoli na łatwy dostęp
# 	do powiązanych obiektów.
	
	body = models.TextField()
# 	body : to pole zawiera treść posta. Jest to pole typu CharField , co odpowiada
#	kolumnie TEXT w bazie danych SQL.

	publish = models.DateTimeField(default = timezone.now)
# 	publish : data i godzina opublikowania posta. Wartość domyślna to metoda now
#	obiektu timezone Django. Metoda zwraca bieżącą datę i godzinę w formacie
#	uwzględniającym strefę czasową. Wartość tę można uważać za wersję standardowej
# 	metody Pythona datetime.now z obsługą stref czasowych.

	created = models.DateTimeField(auto_now_add = True)
# 	created : wartość datetime określająca, kiedy utworzono posta. Ponieważ tutaj
# 	używamy opcji auto_now_add , data zostanie zapisana automatycznie podczas
# 	tworzenia obiektu.

	updated = models.DateTimeField(auto_now = True)
# 	updated : data i godzina ostatniej aktualizacji posta. Ponieważ tutaj używamy opcji
#	auto_now , data zostanie zaktualizowana automatycznie podczas zapisywania obiektu.

	status = models.CharField(max_length = 10,
							  choices = STATUS_CHOICES,
							  default = 'draft')
# 	status : pole zawierające status posta. Używamy parametru choices , więc wartość
# 	tego pola można ustawić tylko na jedną z podanych.


	class Meta:
		ordering = ('-publish',)
# 	Klasa Meta wewnątrz modelu zawiera metadane. Informujemy Django, aby po wysłaniu zapyta-
# 	nia do bazy danych wyniki w polu publish były domyślnie sortowane w porządku malejącym.
# 	Wskazanie kolejności malejącej odbywa się poprzez umieszczenie znaku minus przed prefiksem.
# 	W ten sposób posty opublikowane ostatnio będą wyświetlane jako pierwsze.



	def __str__(self):
		return self.title
# 	Metoda __str__() zwraca domyślną, czytelną dla człowieka reprezentację obiektu. Django używa
# 	jej w wielu miejscach, np. w witrynie administracyjnej.


	objects = models.Manager() # Manager domyślny
	published = PublishedManager() # Manager niestandardowy


	def get_absolute_url(self):
		return reverse('blog:post_detail',
						args = [self.publish.year,
						self.publish.strftime('%m'),
						self.publish.strftime('%d'),
						self.slug])
	# Kanoniczne adresy URL dla modeli
	# Przygotowany wcześniej wzorzec adresu URL dla widoku post_detail możemy wykorzystać
	# do budowy kanonicznych adresów URL dla obiektów Post . Konwencja stosowana w Django
	# polega na dodaniu metody get_absolute_url() do modelu zwracającego kanoniczny adres
	# URL obiektu. W przypadku wymienionej metody wykorzystamy metodę reverse() pozwalającą
	# na utworzenie adresu URL na podstawie nazwy i przekazanie parametrów opcjonalnych.
	# Przeprowadź edycję pliku models.py i umieść w nim wiersze, które w poniższym fragmencie
	# kodu zostały pogrubione.
	# Metodę get_absolute_url() będziemy wykorzystywać w naszych szablonach.

	tags = TaggableManager()


class Comment(models.Model):
	post = models.ForeignKey(Post,
							 on_delete = models.CASCADE,
							 related_name = 'comments')
	# Jest to nasz model Comment . Zawiera klucz zewnętrzny ( ForeignKey ) służący 
	# do połączenia komentarza z odpowiednim postem. W modelu została zdefiniowana 
	# relacja typu „wiele do jednego”, ponieważ każdy komentarz jest przeznaczony 
	# dla jednego konkretnego posta, a sam post może mieć wiele komentarzy. 
	# Atrybut related_name umożliwia nadanie nazwy atrybutowi, którego używamy 
	# do obsługi związku między dwoma obiektami. Po zdefiniowaniu wymienionych
	# aspektów możemy za pomocą comment.post() pobrać obiekt komentarza lub też 
	# użyć post.comments.all() do pobrania wszystkich komentarzy dla danego posta. 
	# Jeśli nie zdefiniujesz atrybutu related_name , Django użyje zapisanej małymi 
	# literami nazwy modelu wraz z przyrostkiem _set (w omawianym przykładzie to 
	# będzie comment_set ) jako menedżera obiektu powiązanego z bieżącym.

	# Więcej informacji na temat relacji typu „wiele do jednego” znajdziesz na 
	# stronie https://docs.djangoproject.com/en/2.0/topics/db/examples/many_to_one/.

	name = models.CharField(max_length = 80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	active = models.BooleanField(default = True)
	# Zdecydowaliśmy się na dołączenie boolowskiego pola active pozwalającego 
	# na ręczne ukrycie nieodpowiedniego komentarza.

	class Meta:
		ordering = ('created',)

		def __str__(self):
			return 'Komentarz dodany przez {} dla posta {}'.format(self.name, self.post)

