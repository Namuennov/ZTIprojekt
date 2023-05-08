from django import forms
from django.forms import ModelForm
from .models import Review, Comment

RATING_CHOICES = (
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
      (6, '6'),
      (7, '7'),
      (8, '8'),
      (9, '9'),
      (10, '10'),
  )

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'rating')
        labels = {
            'content': '',
            'rating': 'Ocena',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'content'}),
            'rating': forms.Select(choices=RATING_CHOICES, attrs={'class': 'form-control'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'content'}),
        }
