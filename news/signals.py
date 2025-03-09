from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *


@receiver(m2m_changed, sender=PostCategory)
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
