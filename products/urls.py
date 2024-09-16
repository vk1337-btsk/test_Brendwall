from django.urls import path

from .apps import ProductsConfig
from .views import ProductCreateView,  ProductPageView


app_name = ProductsConfig.name

urlpatterns = [
    path("", ProductPageView.as_view(), name="product_page"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
]
