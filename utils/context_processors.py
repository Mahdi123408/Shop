from django.db.models import Sum

from products.models import Cart
from utils.auth import check_auth


def cart_summary(request):
    user = check_auth(request)

    if not user[0]:
        return {'cart_count': 0}

    total = Cart.objects.filter(
        user=user[1],
        is_down=False
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return {'cart_count': total}
