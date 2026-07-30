import uuid

from django.contrib.auth import get_user_model

from store.models import ProductModel, ProductVariantModel
from cart.models import CartModel

User = get_user_model()


def create_user():
    return User.objects.create_user(
        username="testuser",
        password="password123",
    )


def create_product():
    return ProductModel.objects.create(
        name="Test Product",
        slug=str(uuid.uuid4()),
        base_price=100000,
        is_active=True,
    )


def create_variant(
    *,
    stock=10,
    is_active=True,
):
    product = create_product()

    return ProductVariantModel.objects.create(
        sku=f"SKU-{uuid.uuid4().hex[:10].upper()}",
        product=product,
        stock=stock,
        is_active=is_active,
    )


def create_cart(
    *,
    session_key="test-session-key",
):
    return CartModel.objects.create(
        session_key=session_key,
    )
