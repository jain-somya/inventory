from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Product, Supplier, SaleOrder, StockMovement
from .forms import ProductForm, SupplierForm, SaleOrderForm, StockMovementForm
from django.http import JsonResponse

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

def list_products(request):
    products = Product.objects.select_related('supplier').all()
    return render(request, 'inventory/list_products.html', {'products': products})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('list_suppliers')
    else:
        form = SupplierForm()
    return render(request, 'inventory/add_supplier.html', {'form': form})

def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/list_suppliers.html', {'suppliers': suppliers})

@transaction.atomic
def create_sale_order(request):
    if request.method == 'POST':
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            sale_order = form.save(commit=False)
            product = sale_order.product
            
            # Check stock availability
            if product.stock_quantity >= sale_order.quantity:
                # Create sale order
                sale_order.save()
                
                # Update stock
                product.stock_quantity -= sale_order.quantity
                product.save()
                
                # Create stock movement
                StockMovement.objects.create(
                    product=product,
                    quantity=sale_order.quantity,
                    movement_type='Out',
                    notes=f'Sale order #{sale_order.id}'
                )
                
                messages.success(request, 'Sale order created successfully!')
                return redirect('list_sale_orders')
            else:
                messages.error(request, 'Insufficient stock!')
    else:
        form = SaleOrderForm()
    return render(request, 'inventory/create_sale_order.html', {'form': form})

@transaction.atomic
def cancel_sale_order(request, order_id):
    sale_order = get_object_or_404(SaleOrder, id=order_id)
    if sale_order.status == 'Pending':
        # Update stock
        product = sale_order.product
        product.stock_quantity += sale_order.quantity
        product.save()
        
        # Update sale order status
        sale_order.status = 'Cancelled'
        sale_order.save()
        
        # Create stock movement
        StockMovement.objects.create(
            product=product,
            quantity=sale_order.quantity,
            movement_type='In',
            notes=f'Cancelled sale order #{sale_order.id}'
        )
        
        messages.success(request, 'Sale order cancelled successfully!')
    return redirect('list_sale_orders')

def check_stock_level(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'stock_quantity': product.stock_quantity})
        return render(request, 'inventory/stock_level.html', {'product': product})
    products = Product.objects.all()
    return render(request, 'inventory/stock_levels.html', {'products': products})
# Add to your existing views.py

def list_sale_orders(request):
    sale_orders = SaleOrder.objects.select_related('product').all().order_by('-sale_date')
    return render(request, 'inventory/list_sale_orders.html', {'sale_orders': sale_orders})

@transaction.atomic
def complete_sale_order(request, order_id):
    sale_order = get_object_or_404(SaleOrder, id=order_id)
    if sale_order.status == 'Pending':
        sale_order.status = 'Completed'
        sale_order.save()
        messages.success(request, 'Sale order completed successfully!')
    return redirect('list_sale_orders')

def list_stock_movements(request):
    stock_movements = StockMovement.objects.select_related('product').all().order_by('-movement_date')
    return render(request, 'inventory/list_stock_movements.html', {'stock_movements': stock_movements})

def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            product = movement.product
            
            # Update stock quantity
            if movement.movement_type == 'In':
                product.stock_quantity += movement.quantity
            else:
                if product.stock_quantity >= movement.quantity:
                    product.stock_quantity -= movement.quantity
                else:
                    messages.error(request, 'Insufficient stock!')
                    return render(request, 'inventory/stock_movement.html', {'form': form})
            
            product.save()
            movement.save()
            messages.success(request, 'Stock movement recorded successfully!')
            return redirect('list_stock_movements')
    else:
        form = StockMovementForm()
    return render(request, 'inventory/stock_movement.html', {'form': form})