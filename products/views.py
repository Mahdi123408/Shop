from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views import View
from products.models import Cart, ProductCategory, Product, ProductMedia
from utils.auth import check_auth
from django.db.models import Prefetch


def _redirect_to_login(request):
    request.session['mes'] = 'برای استفاده از سبد خرید ابتدا وارد حساب کاربری شوید.'
    return redirect('/auth/login/')


def _safe_next_url(request):
    return request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('cart')


class CategoryView(View):
    def get(self, request):

        categories = ProductCategory.objects.filter(
            is_active=True,
            sub_category=None
        ).prefetch_related('sub_categorys')

        mes = None

        if 'mes' in request.session:
            mes = request.session.get('mes')
            del request.session['mes']

        user = check_auth(request)

        context = {
            'categories': categories,
            'mes': mes
        }

        if user[0]:
            context['custom_user'] = user[1]

        return render(request, 'category/category.html', context)

class OneCategoryView(View):

    def get(self, request, slug):

        category = ProductCategory.objects.filter(
            is_active=True,
            slug=slug
        ).first()

        if not category:
            return redirect('/')

        products = Product.objects.filter(
            is_active=True,
            deleted=False,
            category=category
        ).prefetch_related(
            'media'
        ).distinct().order_by('-id')

        paginator = Paginator(products, 50)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        mes = None

        if 'mes' in request.session:
            mes = request.session.get('mes')
            del request.session['mes']

        user = check_auth(request)

        context = {
            'category': category,
            'products': page_obj,
            'page_obj': page_obj,
            'mes': mes
        }

        if user[0]:
            context['custom_user'] = user[1]

        return render(
            request,
            'category/one_category.html',
            context
        )

class ProductsView(View):
    def get(self, request):
        categories = ProductCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter(
                    is_active=True,
                    deleted=False
                ).prefetch_related(
                    Prefetch(
                        'media',
                        queryset=ProductMedia.objects.filter(is_active=True)
                    )
                ).distinct().order_by('-created_at')[:15],
                to_attr='featured_products'
            )
        )

        mes = None
        if 'mes' in request.session:
            mes = request.session.get('mes')
            del request.session['mes']

        user = check_auth(request)

        context = {
            'categories': categories,
            'mes': mes,
        }

        if user[0]:
            context['custom_user'] = user[1]

        return render(request, 'products/products.html', context)


class CartView(View):
    def get(self, request):
        user = check_auth(request)
        if not user[0]:
            return _redirect_to_login(request)

        mes = None
        if 'mes' in request.session:
            mes = request.session.get('mes')
            del request.session['mes']

        cart_items = Cart.objects.filter(
            user=user[1],
            is_down=False
        ).select_related(
            'product'
        ).prefetch_related(
            'product__media'
        ).order_by('-updated_at')

        subtotal = sum(item.line_total for item in cart_items)

        context = {
            'custom_user': user[1],
            'cart_items': cart_items,
            'subtotal': subtotal,
            'mes': mes,
        }

        return render(request, 'cart/cart.html', context)


class AddToCartView(View):
    def post(self, request, product_id):
        user = check_auth(request)
        if not user[0]:
            return _redirect_to_login(request)

        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True,
            deleted=False
        )

        try:
            quantity = max(int(request.POST.get('quantity', 1)), 1)
        except ValueError:
            quantity = 1

        if product.count_inventory <= 0:
            request.session['mes'] = 'این محصول موجود نیست.'
            return redirect(_safe_next_url(request))

        cart_item, created = Cart.objects.get_or_create(
            user=user[1],
            product=product,
            is_down=False,
            defaults={'quantity': 0}
        )

        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.count_inventory:
            cart_item.quantity = product.count_inventory
            cart_item.save(update_fields=['quantity', 'updated_at'])
            request.session['mes'] = 'تعداد درخواستی بیشتر از موجودی محصول بود.'
            return redirect(_safe_next_url(request))

        cart_item.quantity = new_quantity
        cart_item.save(update_fields=['quantity', 'updated_at'])
        request.session['mes'] = 'محصول به سبد خرید اضافه شد.'

        return redirect(_safe_next_url(request))


class UpdateCartItemView(View):
    def post(self, request, item_id):
        user = check_auth(request)
        if not user[0]:
            return _redirect_to_login(request)

        cart_item = get_object_or_404(
            Cart,
            id=item_id,
            user=user[1],
            is_down=False
        )

        action = request.POST.get('action')

        if action == 'increase':
            if cart_item.quantity < cart_item.product.count_inventory:
                cart_item.quantity += 1
                cart_item.save(update_fields=['quantity', 'updated_at'])
            else:
                request.session['mes'] = 'موجودی این محصول بیشتر از این نیست.'
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save(update_fields=['quantity', 'updated_at'])
        else:
            try:
                quantity = max(int(request.POST.get('quantity', 1)), 1)
            except ValueError:
                quantity = 1
            cart_item.quantity = min(quantity, cart_item.product.count_inventory)
            cart_item.save(update_fields=['quantity', 'updated_at'])

        return redirect('cart')


class RemoveCartItemView(View):
    def post(self, request, item_id):
        user = check_auth(request)
        if not user[0]:
            return _redirect_to_login(request)

        Cart.objects.filter(
            id=item_id,
            user=user[1],
            is_down=False
        ).delete()

        request.session['mes'] = 'محصول از سبد خرید حذف شد.'
        return redirect('cart')


class ClearCartView(View):
    def post(self, request):
        user = check_auth(request)
        if not user[0]:
            return _redirect_to_login(request)

        Cart.objects.filter(user=user[1], is_down=False).delete()
        request.session['mes'] = 'سبد خرید خالی شد.'
        return redirect('cart')


class CheckoutView(View):
    def post(self, request):
        user = check_auth(request)
        if not user[0]:
            return _redirect_to_login(request)

        with transaction.atomic():
            cart_items = list(
                Cart.objects.select_for_update().filter(
                    user=user[1],
                    is_down=False
                ).select_related('product')
            )

            if not cart_items:
                request.session['mes'] = 'سبد خرید شما خالی است.'
                return redirect('cart')

            for item in cart_items:
                if item.quantity > item.product.count_inventory:
                    request.session['mes'] = f'موجودی {item.product.title} کافی نیست.'
                    return redirect('cart')

            for item in cart_items:
                product = item.product
                product.count_inventory -= item.quantity
                product.save(update_fields=['count_inventory', 'updated_at'])

                item.price = product.price
                item.discount = product.discount
                item.is_down = True
                item.save(update_fields=['price', 'discount', 'is_down', 'updated_at'])

        request.session['mes'] = 'خرید با موفقیت ثبت شد.'
        return redirect('cart')

