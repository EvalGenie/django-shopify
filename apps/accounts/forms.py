# accounts - forms.py
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django import forms

from apps.authentication.models import CustomUser


class EditProfileForm(forms.ModelForm):
    # email = forms.
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'rank', 'gender')
