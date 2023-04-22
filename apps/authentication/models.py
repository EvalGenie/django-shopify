# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps import COMMON

# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NS', 'Not Specified')
    )
    
    RANK_CHOICES = (
        #ENLISTED
        ('SGT', 'Sergeant'),
        ('SSG', 'Staff Sergeant'),
        ('SFC', 'Sergeant First Class'),
        ('MSG', 'Master Sergeant'),
        ('1SG', 'First Sergeant'),
        ('SGM', 'Sergeant Major'),
        ('CSM', 'Command Sergeant Major'),
        ('SMA', 'Sergeant Major of the Army'),
        #OFFICERS
        ('2LT', 'Second Lieutenant'),
        ('1LT', 'First Lieutenant'),
        ('CPT', 'Captain'),
        ('MAJ', 'Major'),
        ('LTC', 'Lieutenant Colonel'),
        ('COL', 'Colonel'),
        ('BG', 'Brigadier General'),
        ('MG', 'Major General'),
        ('LTG', 'Lieutenant General'),
        ('GEN', 'General'),
        ('GOA', 'General of the Army'),
        #WARRANT OFFICERS (Best for last)
        ('CW1', 'Warrant Officer 1'),
        ('CW2', 'Chief Warrant Officer 2'),
        ('CW3', 'Chief Warrant Officer 3'),
        ('CW4', 'Chief Warrant Officer 4'),
        ('CW5', 'Chief Warrant Officer 5'),
    )

    failed_logins     = models.IntegerField(default=0)
    tokens            = models.IntegerField(default=10)
    status            = models.IntegerField(default=COMMON.USER_ACTIVE)
    phone             = models.CharField(max_length=20,default='', blank=True)
    registration_date = models.DateField(auto_now=True)
    image             = models.URLField(default='')
    gender            = models.CharField(max_length=2, choices=GENDER_CHOICES, default='NS')
    rank              = models.CharField(max_length=3, choices=RANK_CHOICES, default='E1')