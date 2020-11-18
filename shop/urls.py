from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('brand/<int:brand_slug>/', views.brand_detail,
         name='product_list_by_brand'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),

    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]
