import json

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import ProductForm
from .models import Product


class ProductPageView(TemplateView):
    """Представление для отображения списка продуктов."""

    template_name = "products/product_list.html"


class ProductCreateView(CreateView):
    """Представление для создания продукта."""

    form_class = ProductForm
    success_url = reverse_lazy("product_page")

    def form_invalid(self, form):
        errors = {field: error.get_json_data() for field, error in form.errors.items()}
        print(errors)
        return JsonResponse({"error-message": errors}, status=400)

    def form_valid(self, form):
        self.object = form.save()
        product_data = {
            "id": self.object.id,
            "name": self.object.name,
            "description": self.object.description,
            "price": self.object.price,
        }
        return JsonResponse({"success-message": "Продукт успешно создан", "product": product_data}, status=201)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Для отладки
            form = self.get_form_class()(data)

            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        except json.JSONDecodeError:
            return JsonResponse({"error-message": "Некорректный формат данных"}, status=400)
        except Exception as e:
            return JsonResponse({"error-message": str(e)}, status=400)
