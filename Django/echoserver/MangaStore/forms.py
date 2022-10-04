from django import forms

class MangaForm(forms.Form):
    name = forms.CharField(max_length=30, label="Manga", initial="BaseName", required=True)
    author = forms.CharField(max_length=30, label="Author", initial="BaseAuthorName", required=True)
    price = forms.FloatField(min_value = 0, initial=0.0, help_text="enter a non-negative number", required=True)