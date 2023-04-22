# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django.contrib import admin
from .models import Accomplishment, Room, Message

# Register your models here.
admin.site.register(Accomplishment)
admin.site.register(Room)
admin.site.register(Message)