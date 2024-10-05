import stripe
from django import template

from paid_content_app.models import PurchasedPost

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f'/media/{path}'
    else:
        return '#'


@register.filter
def is_purchased(post, user):
    purchased_posts = PurchasedPost.objects.filter(post=post, user=user)
    for i in purchased_posts:
        response = stripe.checkout.Session.retrieve(i.session_id)
        if response.status == 'complete':
            return True
    return False
