from calendar import c
from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, Select
from .models import Listing

class ListingForm(ModelForm):

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
            }),
            'description': Textarea(attrs={
                'class': 'form-control'
            }),
            'starting_bid': NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01'
            }),
            'image_url': URLInput(attrs={
                'class': 'form-control'
            }),
            'category': Select(attrs={
                'class': 'form-control'
            })
        }