from django import forms
from core.models import ProductReview
from django.shortcuts import get_object_or_404, render, HttpResponse


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':  'Write your review here...'}))
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
