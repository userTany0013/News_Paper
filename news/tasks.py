from datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils import timezone


from .models import *


def send_mails():
    for i in Category.objects.all():
        address_list = []
        cat = i.id
        user_list = SubscribCategory.objects.filter(category=cat)
        timezone.now()
        q = datetime.now()
        q_1 = q - timedelta(weeks=1)
        week_list = []
        for w in Post.objects.all():
            if w.date_time >= q_1:
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

