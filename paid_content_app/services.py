import os

import stripe
from django.conf import settings
from dotenv import load_dotenv
from smsaero import SmsAero

from config.settings import BASE_DIR

load_dotenv(BASE_DIR / '.env', override=True)
stripe.api_key = os.getenv('stripe_api_key')


def create_product(post):
    """Создает продукт"""
    return stripe.Product.create(name=f"{post.name}")


def create_price(post, product):
    """Создает цену в stripe."""
    return stripe.Price.create(
        currency=post.currency,
        unit_amount=post.price * 100,
        product=product.get('id')
    )


def create_session(post, price):
    """Создает сессию для оплаты"""
    session = stripe.checkout.Session.create(
        success_url=f"http://127.0.0.1:8000/post/{post.id}/check_payment/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def send_sms(phone: str, message: str) -> dict:
    """
    Sends an SMS message

    Parameters:
    phone (int): The phone number to which the SMS message will be sent.
    message (str): The content of the SMS message to be sent.

    Returns:
    dict: A dictionary containing the response from the SmsAero API.
    """
    if phone[0] == '8':
        phone = '7' + phone[1:]
    phone = int(phone)
    api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
    return api.send_sms(phone, message)
