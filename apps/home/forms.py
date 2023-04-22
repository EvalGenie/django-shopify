# home - forms.py
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""
from django import forms
from .models import Accomplishment

class AccomplishmentForm(forms.ModelForm):
    class Meta:
        model = Accomplishment
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter accomplishment details'}),
        }
        labels = {
            'description': 'Accomplishment',
        }

class EditAccomplishmentForm(forms.ModelForm):
    class Meta:
        model = Accomplishment
        fields = ('id', 'description',)