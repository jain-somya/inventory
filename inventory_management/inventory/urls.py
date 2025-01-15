# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/add/', views.add_product, name='add_product'),
    path('products/', views.list_products, name='list_products'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/', views.list_suppliers, name='list_suppliers'),
    path('sales/create/', views.create_sale_order, name='create_sale_order'),
    path('sales/cancel/<int:order_id>/', views.cancel_sale_order, name='cancel_sale_order'),
    path('stock/check/', views.check_stock_level, name='check_stock_level'),
    path('stock/check/<int:product_id>/', views.check_stock_level, name='check_product_stock'),
    path('sales/', views.list_sale_orders, name='list_sale_orders'),
    path('sales/complete/<int:order_id>/', views.complete_sale_order, name='complete_sale_order'),
    path('stock/movements/', views.list_stock_movements, name='list_stock_movements'),
    path('stock/movements/add/', views.add_stock_movement, name='add_stock_movement'),
]