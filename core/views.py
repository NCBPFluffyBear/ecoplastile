from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# For the warnings ^
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress

# Create your views here.


""" def HomeView(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context) """


""" def ProductView(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product-page.html", context) """


# either primary key or slug
class ProductView(DetailView):
    model = Item
    template_name = "product-page.html"


class HomeView(ListView):
    model = Item
    # How many items per page
    paginate_by = 10
    template_name = "home-page.html"


# View as we do not want to inherit a slug or pk
class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwards):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(
                self.request, "You do not have any items in the cart")
            return redirect("/")


# def CheckoutView(request):
#     return render(request, "checkout-page.html", {})

class CheckoutView(View):
    def get(self, *args, **kwargs):
        # The form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout-page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # print(form.cleaned_data)
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                # TODO
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: redirect payment
                return redirect('core:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any items in the cart")
            return redirect("core:order-summary")
        # print(self.request.POST)



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # avoid recreating the item to declutter log
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    # Only take the uncompleted order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # see if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The item quantity has been updated.")
            return redirect("core:order-summary")
        else:
            # Adding different tokens
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        # New Order
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # see if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                order.items.remove(order_item)
                order_item.delete()
            order_item.save()

            messages.info(request, "The item quantity has been updated.")
            return redirect("core:order-summary")
        else:
            # User does not contain does item
            messages.info(request, "This item is not in your cart.")
            return redirect("core:Product", slug=slug)
    else:
        # User has no orders
        messages.info(request, "There are no items in your cart.")
        return redirect("core:Product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # see if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            # Remove the object - or else it will think it has 1
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            # User does not contain does item
            messages.info(request, "This item is not in your cart.")
            return redirect("core:Product", slug=slug)
    else:
        # User has no orders
        messages.info(request, "There are no items in your cart.")
        return redirect("core:Product", slug=slug)


""" from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order

# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product-page.html", context)


class ItemView(DetailView):
    model = Item
    template_name = "product-page.html"
"""
