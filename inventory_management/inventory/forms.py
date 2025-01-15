# inventory/forms.py
from django import forms
from .models import Product, Supplier, SaleOrder, StockMovement

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ProductForm(BaseForm):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierForm(BaseForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class SaleOrderForm(BaseForm):
    class Meta:
        model = SaleOrder
        fields = ['product', 'quantity']

class StockMovementForm(BaseForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'movement_type', 'notes']