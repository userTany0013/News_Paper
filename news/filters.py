import django_filters
from django.forms import DateInput
from django_filters import FilterSet, ModelMultipleChoiceFilter

from .models import Post, Author


class PostFilter(FilterSet):
    author = ModelMultipleChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
    )
    date_time = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date', 'field': 'date_time'}),
                                          lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {
            "heading": ['icontains'],
        }
