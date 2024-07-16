from django import forms

class GuessForm(forms.Form):
    guess = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
