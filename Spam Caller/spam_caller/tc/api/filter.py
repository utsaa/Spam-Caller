from django_filters import FilterSet
import django_filters
from tc.models import Phone

class ListFilter(FilterSet):
    phone=django_filters.CharFilter(field_name='phone')
    user=django_filters.CharFilter(field_name='user__username')
    class Meta:
        model=Phone
        fields=['user', 'phone']
