from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *


def send_mails():
    for i in Category.objects.all():
        address_list = []
        cat = i.id
        user_list = SubscribCategory.objects.filter(category=cat)
        week_list = []
        for w in Post.objects.all():
            q = q = timezone.now()
            if q - w.date_time < timedelta(weeks=1):
                week_list.append(w)
        for y in user_list:
            user = y.user
            user_e = User.objects.get(username=user)
            address_list.append(user_e.email)
        html_content = render_to_string(
            'week.html',
            {
                'y': week_list
            }
        )
        msg = EmailMultiAlternatives(
            subject='',
            from_email='Tany911922@yandex.ru',
            to=address_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def new_post_message(sender, instance, **kwargs):
    address_list = []
    cat = instance.category.all()
    for i in cat:
        cat_obj = SubscribCategory.objects.filter(category=i.id)
        for o in cat_obj:
            user_obj = o.user
            address_list.append(user_obj.email)
            html_content = render_to_string(
                'massage.html',
                {
                    'instance': instance,
                    'user_obj': user_obj,
                    'text': instance.text[:50],
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.heading,
                from_email='Tany911922@yandex.ru',
                to=address_list
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

