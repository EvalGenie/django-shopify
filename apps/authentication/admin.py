# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django.contrib import admin
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser)