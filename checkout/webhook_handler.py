'''
Set up Stripe webhooks handler: if checkout fails,
the webhook handler will execute all the expected functionalities.
(payment processing, save order and profile info)
'''

import json
import time

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from products.models import Product
from .models import Order, OrderLineItem


class StripeWebhookHandler:
    ''' Handle Stripe Webhooks '''

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        ''' Send the user a confirmation email'''
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def _update_product_quantity_sold(self, order):
        ''' update the quantity sold field for the products ordered '''
        order_line_items = order.lineitems.all()
        for item in order_line_items:
            product = get_object_or_404(Product, pk=item.product.id)
            quantity_sold = product.quantity_sold
            total_quantity_sold = quantity_sold + item.quantity
            product.quantity_sold = total_quantity_sold
            product.save()

    def handle_event(self, event):
        ''' Hanlde a generic/unknown/unexpected webhook event '''
        return HttpResponse(
            content=f'Unhandled webhook received {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        ''' Hanlde the payment_intent.succeed webhook from stripe '''
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details to match database value
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_full_name = shipping_details.name
                profile.default_email = billing_details.email
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = \
                    shipping_details.address.line1
                profile.default_street_address2 = \
                    shipping_details.address.line2
                profile.default_county_or_region = \
                    shipping_details.address.state
                profile.save()

        # Look if the order exist in DB already,
        # Try 5 time for 5sec in order to give time
        # for the webhook to create the order (creates delay)
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county_or_region__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._update_product_quantity_sold(order)
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received {event["type"]} | \
                              SUCCESS: Verified order already in the database',
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county_or_region=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received {event["type"]} \
                                              | ERROR: {e}', status=500)

        self._update_product_quantity_sold(order)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received {event["type"]} | \
                      SUCCESS: Created in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        ''' Hanlde the payment_intent.payment_failed webhook from stripe '''
        return HttpResponse(
            content=f'Payment failed Webhook received {event["type"]}',
            status=200)
