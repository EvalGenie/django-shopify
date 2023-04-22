# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django.urls import path, re_path, include
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.checkout, name='success'),
    path('cancel/', views.checkout, name='cancel'),
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('ajax/get_chat_history/<int:room_id>/', views.get_chat_history, name='get_chat_history'),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
