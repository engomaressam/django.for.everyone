from django import forms
from ads.models import Ad, Comment

class CreateForm(forms.ModelForm):
    # File upload field is optional
    file = forms.FileField(required=False, label='Select a file')

    class Meta:
        model = Ad
        fields = ['title', 'price', 'text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
