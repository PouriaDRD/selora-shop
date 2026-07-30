import uuid

from store.models import (
    CategoryModel,
    ProductModel,
    ProductVariantModel,
    AttributeModel,
    AttributeValueModel,
)


def create_category(name="Electronics"):
    return CategoryModel.objects.create(
        name=f"{name}-{uuid.uuid4().hex[:6]}",
    )


def create_product(
    category=None,
    name="Laptop",
    price=1000,
):

    return ProductModel.objects.create(
        name=f"{name}-{uuid.uuid4().hex[:6]}",
        category=category,
        base_price=price,
        description="Test product",
    )


def create_variant(
    product,
    sku=None,
    stock=10,
    active=True,
    price_override=None,
):

    return ProductVariantModel.objects.create(
        product=product,
        sku=sku or f"SKU-{uuid.uuid4().hex[:8]}",
        stock=stock,
        is_active=active,
        price_override=price_override,
    )


def create_attribute():

    return AttributeModel.objects.create(name=f"Color-{uuid.uuid4().hex[:5]}")


def create_attribute_value(attribute):

    return AttributeValueModel.objects.create(
        attribute=attribute,
        value="Red",
    )
