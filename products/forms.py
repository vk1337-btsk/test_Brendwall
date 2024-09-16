from django import forms

from .models import Product


class StyleFormMixin:
    """Класс-миксин для стиля формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs["class"] = "form-control flatpickr-basic"
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["class"] = "form-control"
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs["class"] = "form-control datepicker"
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs["class"] = "form-control flatpickr-time"
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs["class"] = "form-control select2 select2-multiple"
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs["class"] = "form-control select2"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(forms.ModelForm):
    """Форма для создания продуктов."""
    
    class Meta:
        model = Product
        fields = ["name", "description", "price"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name.strip():
            raise forms.ValidationError("Название продукта не может быть пустым.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description.strip():
            raise forms.ValidationError("Описание продукта не может быть пустым.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Стоимость продукта должна быть положительной и не может быть равна 0.")
        return price
