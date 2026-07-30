from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from store.models import ProductVariantModel

from .factories import (
    create_category,
    create_product,
    create_variant,
    create_attribute,
    create_attribute_value,
)


class CategoryAPITest(APITestCase):

    def test_category_list(self):

        create_category()

        url = reverse("category-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            len(response.data),  # type: ignore
            1,
        )

    def test_category_with_products(self):

        category = create_category()

        product = create_product(
            category=category,
        )

        url = reverse(
            "category-detail",
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        category_data = response.data[0]  # type: ignore

        self.assertEqual(
            category_data["name"],
            category.name,
        )

        self.assertEqual(
            len(category_data["products"]),
            1,
        )

        self.assertEqual(
            category_data["products"][0]["id"],
            str(product.id),
        )


class ProductAPITest(APITestCase):

    def test_product_list(self):

        product = create_product()

        url = reverse(
            "product-list",
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(any(item["id"] == str(product.id) for item in response.data))  # type: ignore

    def test_product_detail_contains_variants(self):

        product = create_product()

        variant = create_variant(
            product=product,
            stock=5,
        )

        url = reverse(
            "product-detail",
            kwargs={
                "slug": product.slug,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        variants = response.data["variants"]  # type: ignore

        self.assertEqual(
            len(variants),
            1,
        )

        self.assertEqual(
            variants[0]["sku"],
            variant.sku,
        )


class VariantSerializerTest(APITestCase):

    def test_variant_price_override(self):

        product = create_product(
            price=500,
        )

        variant = create_variant(
            product=product,
            price_override=300,
        )

        url = reverse(
            "product-detail",
            kwargs={
                "slug": product.slug,
            },
        )

        response = self.client.get(url)

        variant_data = response.data["variants"][0]  # type: ignore

        self.assertEqual(
            variant_data["price"],
            300,
        )


class AttributeSerializerTest(APITestCase):

    def test_attribute_contains_values(self):

        attribute = create_attribute()

        value = create_attribute_value(
            attribute,
        )

        from store.api.v1.serializers import AttributeSerializer

        data = AttributeSerializer(attribute).data

        self.assertEqual(
            data["name"],  # type: ignore
            attribute.name,
        )

        self.assertEqual(
            data["values"][0]["value"],  # type: ignore
            value.value,
        )
