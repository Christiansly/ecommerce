from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
 url = reverse('orders:admin_order_pdf', args=[obj.id])
 return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'

def order_detail(obj):
 url = reverse('orders:admin_order_detail', args=[obj.id])
 return mark_safe(f'<a href="{url}">View</a>')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
