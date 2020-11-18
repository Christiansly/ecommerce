from django.conf import settings
import weasyprint
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
# Create your views here.

from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], size=item['size'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
            
    else:
        print(request.user.first_name)
        form = OrderCreateForm(initial={
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'address':request.user.profile.address,
            'postal_code':request.user.profile.postal_code,
            'city':request.user.profile.city,
        }
            
        )
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/details.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
 order = get_object_or_404(Order, id=order_id)
 html = render_to_string('orders/order/pdf.html',
                         {'order': order})
 response = HttpResponse(content_type='application/pdf')
 response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
 weasyprint.HTML(string=html).write_pdf(response,
                                        stylesheets=[weasyprint.CSS(
     settings.STATIC_ROOT + 'css/pdf.css')])
 return response
