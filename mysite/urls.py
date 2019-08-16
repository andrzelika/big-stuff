"""mysite URL Configuration

urls.py: w tym pliku są zapisane wzorce adresów URL, każdy zdefiniowany
tutaj adres URL jest zmapowany na widok;

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Administration page'
admin.site.site_title = 'SiteTitle admin'
admin.site.index_title = 'Zarządzaj zawartością strony'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
	# Nowy wzorzec adresu URL zdefiniowany za pomocą include odnosi się do wzorców adresów
	# URL zdefiniowanych w aplikacji blog , dlatego zostały dołączone w ścieżce blog/ . Te wzorce
	# dołączamy w ramach przestrzeni nazw blog . Przestrzenie nazw muszą być unikatowe w całym
	# projekcie. Później możemy łatwo odwoływać się do adresów URL naszego bloga za pomocą
	# przestrzeni nazw. Adres URL może przyjąć np. format blog: post_list lub blog:post_detail .
	# Więcej informacji na temat przestrzeni nazw URL można znaleźć pod adresem https://docs.
	# djangoproject.com/en/2.0/topics/http/urls/#urlnamespaces.
]
