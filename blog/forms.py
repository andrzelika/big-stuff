# Django dostarcza dwie klasy bazowe przeznaczone do tworzenia formularzy.
# 	- Form - 	  Klasa jest przeznaczona do budowania formularzy standardowych.
# 	- ModelForm - Klasa jest przeznaczona do budowania formularzy, za pomocą których
# 				  będą tworzone lub uaktualniane egzemplarze modelu.

from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
	name = forms.CharField(max_length = 25)
	email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required = False,
							    widget = forms.Textarea)
	# W polu comments użyliśmy widżetu Textarea do wyświetlania go jako elementu HTML 
	# <textarea> zamiast jako domyślnego elementu <input>.

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')
