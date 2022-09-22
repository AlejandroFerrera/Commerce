from calendar import c
from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, Select
from django.core.validators import MinValueValidator
from .models import Listing


class ListingForm(ModelForm):

    starting_bid = forms.DecimalField(
        max_digits=9, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'category', 'starting_bid']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
            'image_url': URLInput(attrs={
                'class': 'form-control'
            }),
            'category': Select(attrs={
                'class': 'form-control'
            })
        }
    
    field_order = ['title', 'category', 'description', 'starting_bid', 'image_url']
