from django import template
from core.models import Order

# Allows us to see how much items in the cart


# Registers the template tag
register = template.Library()


@register.filter
def crt_itm_cnt(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
