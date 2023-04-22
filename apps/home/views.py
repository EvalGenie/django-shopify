# home - views.py
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django import template
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from apps import COMMON
from apps.authentication.models import CustomUser
from .models import Accomplishment as acc
from .models import UserPayment, Room, Message
from apps.home.forms import AccomplishmentForm
from paypal.standard.forms import PayPalPaymentsForm
import stripe
from django.conf import settings
import uuid
import time
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.core import serializers


@login_required(login_url="/login/")
def index(request):
    user = CustomUser.objects.get(username=request.user.username)
    # Query the database for all accomplishments owned by this user
    accomplishments = acc.objects.filter(user=request.user, status='A').order_by('-creation_date')[:5]
    count = acc.objects.filter(user=request.user, status='A').count()

    if user.status == COMMON.USER_SUSPENDED:
        logout(request)
        return redirect(reverse(f'login') + f'?message=Suspended account. Please contact support.')

    context = {
        'segment': 'index',
        'tokens': user.tokens,
        'recent_accomplishments': accomplishments,
        'count': count,
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]
        
        #
        # Admin Page
        #
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        
        #
        # NCOER Bullet Generator
        #
        if load_template == 'bullet-generator.html':
            if request.method == 'GET':
                sessions = Room.objects.filter(user=request.user, status='A', catagory='B').order_by('-creation_date')
                context = {'user': request.user, 'sessions':sessions}
                return render(request, 'home/bullet-generator.html', context)
            
            if request.method == 'POST':
                if request.POST.get('marker') == 'NewSession':
                    new_session = Room(user=request.user, catagory='B', status='A')
                    new_session.save()
                    
                    sessions = Room.objects.filter(user=request.user, status='A', catagory='B').order_by('-creation_date')
                    context = {'user': request.user, 'sessions':sessions}
                    return render(request, 'home/bullet-generator.html', context)
        #
        # Storefront
        #
        if load_template == 'shop.html':
            if request.method == 'GET':
                context = {}
                return render(request, 'home/shop.html', context)
        #
        # Accomplishment Journal
        #
        if load_template == 'accomplishment-journal.html':
            if request.method == 'GET':
                # Query the database for all accomplishments owned by this user
                accomplishments = acc.objects.filter(user=request.user, status='A').order_by('-creation_date')
        
                # Pass the accomplishments to the context dictionary
                context['accomplishments'] = accomplishments
        
                # Render the template with the context data
                return render(request, 'home/accomplishment-journal.html', context)

            if request.method == 'POST':
                if request.POST.get('marker') == 'Save':
                    print('POST Save')
                    description = request.POST.get('description')
                    accomplishment = acc(description=description, user=request.user)
                    accomplishment.save()
                    accomplishments = acc.objects.filter(user=request.user, status='A').order_by('-creation_date')
                    context['accomplishments'] = accomplishments
                    return render(request, 'home/accomplishment-journal.html', context)
                
                if request.POST.get('marker') == 'Delete':
                    print('POST Delete')
                    accomplishment_id = request.POST.get('record-id')
                    accomplishment = acc.objects.get(pk=accomplishment_id, user=request.user)
                    accomplishment.status = 'R'
                    accomplishment.save()
                    accomplishments = acc.objects.filter(user=request.user, status='A').order_by('-creation_date')
                    context['accomplishments'] = accomplishments
                    return render(request, 'home/accomplishment-journal.html', context)
                
                if request.POST.get('marker') == 'Edit':
                    print('POST Edit')
                    accomplishment_id = request.POST.get('record-id')
                    print(accomplishment_id)
                    edit_description = request.POST.get('edit_description')
                    print(edit_description)
                    accomplishment = acc.objects.get(pk=accomplishment_id, user=request.user)
                    accomplishment.description = edit_description
                    accomplishment.save()
                    accomplishments = acc.objects.filter(user=request.user, status='A').order_by('-creation_date')
                    context['accomplishments'] = accomplishments
                    return render(request, 'home/accomplishment-journal.html', context)
    
    # Error Handling
    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url='/login/')
def checkout(request):
    context = {}
    stripe.api_key = settings.STRIPE_SECRET
    #TODO: Add try/except error handling.y
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1MqRSvFUu5u4xS0rcit6UV8g',
                    'quantity': 1,
                },
            ],
            mode='payment',
            #TODO: These URLS are not correct and needs to be adjusted for the domain.
            success_url='http://44.199.246.183:8000' + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://44.199.246.183:8000' + '/payment_cancelled',
            )
        return redirect(checkout_session.url, code=303)
    return render(request, 'home/shop.html', context)

# This view is for when a purchange has been successfully made through the shop.
# TODO: Provide a  notification to the user that the transaction was successful.
@login_required(login_url='/login/')
def success(request):
    stripe.api_key = settings.STRIPE_SECRET
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user
    user_payment = UserPayment.object.get(app_user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    
    return render(request, 'home/payment_successful.html', {'customer':customer})

# This view is for when a purchase has been cancelled and the user has been returned to the main dashboard
# TODO: Provide a notification to the user that the transation was canceled.
@login_required(login_url='/login/')
def cancel(request):
    return render(request, 'home')

# This view is a webhook catch for Stripe so that we can confirm a user's purchase
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
            )
    except ValueError as e:
        print('Stripe Webhook ValueError')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Stripe Signature Verification Error')
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print('Stripe Webhook Session:', session)
        session_id = session.get('id', None)
        print('Stripe Webhook Session ID:', session_id)
        time.sleep(15)
        user_payment = UserPayment.object.get(stripe_checkout_id = session)
        user_payment.payment_bool = True
        user_payment.save()
        print('Stripe Webhook Updated Database Payment to True')
    return HttpResponse(status=200)

@login_required(login_url='/login/')
def get_chat_history(request, room_id):
    if request.method == "GET" and request.is_ajax():
        messages = Message.objects.filter(room__id=room_id).order_by('creation_date')
        messages_serialized = serializers.serialize('json', messages)
        return JsonResponse({"messages": messages_serialized}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)
    