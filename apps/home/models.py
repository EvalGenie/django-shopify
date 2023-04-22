# home - models.py
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from decimal import Decimal

# Create your models here.
class Room(models.Model):
    CATAGORY = (
        ('N', 'Not Specified'),
        ('D', 'Daily Duties and Scope'),
        ('B', 'Bullet'),
        ('C', 'Comment'),
    )
    
    STATUS = (
        ('N', 'Not Specified'),
        ('A', 'Active'),
        ('R', 'Archived')
    )
    
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    catagory = models.CharField(max_length=1, choices=CATAGORY, default='N')
    status = models.CharField(max_length=1, choices=STATUS, default='N')
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('creation_date',)

class Accomplishment(models.Model):
    STATUS = (
        ('A', 'Active'),
        ('R', 'Removed'),
        ('N', 'Archived')
    )
    
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default='A')

# Payment Processing Model for Stripe.
# This helps to verify customers paid for the product/service via Stripe Webhook
class UserPayment(models.Model):
    app_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)