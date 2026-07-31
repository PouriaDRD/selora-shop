import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw

from store.models import (
    AttributeModel,
    AttributeValueModel,
    CategoryModel,
    ProductModel,
    ProductImageModel,
    ProductVariantModel,
)


def make_placeholder_image(text: str, color: tuple[int, int, int]):
    image = Image.new(
        "RGB",
        (600, 600),
        color=color,
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (40, 280),
        text,
        fill="white",
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    return ContentFile(
        buffer.getvalue(),
        name=f"{text}.png",
    )


PALETTE = [
    (200, 60, 60),
    (60, 120, 200),
    (60, 160, 90),
    (180, 140, 40),
    (120, 80, 160),
    (40, 150, 150),
]


class Command(BaseCommand):
    help = "Seed demo store data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing store data",
        )

    @transaction.atomic
    def handle(self, *args, **options):

        if options["flush"]:
            ProductVariantModel.objects.all().delete()
            ProductImageModel.objects.all().delete()
            ProductModel.objects.all().delete()
            AttributeValueModel.objects.all().delete()
            AttributeModel.objects.all().delete()
            CategoryModel.objects.all().delete()

            self.stdout.write(self.style.WARNING("Store data cleared."))

        # ==========================
        # Attributes
        # ==========================

        color_attr, _ = AttributeModel.objects.get_or_create(name="Color")

        size_attr, _ = AttributeModel.objects.get_or_create(name="Size")

        colors = {}

        for value in [
            "Black",
            "White",
            "Red",
            "Blue",
        ]:
            colors[value], _ = AttributeValueModel.objects.get_or_create(
                attribute=color_attr,
                value=value,
            )

        sizes = {}

        for value in [
            "S",
            "M",
            "L",
            "XL",
        ]:
            sizes[value], _ = AttributeValueModel.objects.get_or_create(
                attribute=size_attr,
                value=value,
            )

        # ==========================
        # Categories
        # ==========================

        apparel, _ = CategoryModel.objects.get_or_create(
            slug="apparel",
            defaults={
                "name": "پوشاک",
            },
        )

        accessories, _ = CategoryModel.objects.get_or_create(
            slug="accessories",
            defaults={
                "name": "اکسسوری",
            },
        )

        home, _ = CategoryModel.objects.get_or_create(
            slug="home-decoration",
            defaults={
                "name": "خانه و دکوراسیون",
            },
        )

        # ==========================
        # Products
        # ==========================

        products = [
            {
                "name": "تیشرت مینیمال نخی",
                "slug": "minimal-cotton-tshirt",
                "category": apparel,
                "price": 100_000,
                "description": (
                    "تیشرت ساده و سبک با پارچه نخی باکیفیت، "
                    "مناسب استفاده روزمره و استایل مینیمال."
                ),
                "has_color": True,
                "has_size": True,
            },
            {
                "name": "هودی کلاسیک اورسایز",
                "slug": "classic-oversize-hoodie",
                "category": apparel,
                "price": 250_000,
                "description": (
                    "هودی گرم و راحت با طراحی مدرن، " "مناسب فصل پاییز و زمستان."
                ),
                "has_color": True,
                "has_size": True,
            },
            {
                "name": "ماگ سرامیکی مینیمال",
                "slug": "minimal-ceramic-mug",
                "category": home,
                "price": 125_000,
                "description": (
                    "ماگ سرامیکی ساده و شیک " "برای خانه، محل کار و استفاده روزانه."
                ),
                "has_color": True,
                "has_size": False,
            },
            {
                "name": "اکسسوری دکوراتیو",
                "slug": "decorative-accessory",
                "category": accessories,
                "price": 180_000,
                "description": (
                    "اکسسوری کوچک و کاربردی " "برای تکمیل زیبایی فضای داخلی."
                ),
                "has_color": True,
                "has_size": False,
            },
            {
                "name": "بالشت دکوراتیو نرم",
                "slug": "soft-decorative-pillow",
                "category": home,
                "price": 240_000,
                "description": (
                    "بالشت نرم و راحت با طراحی زیبا " "برای دکوراسیون مدرن منزل."
                ),
                "has_color": False,
                "has_size": False,
            },
        ]

        # ==========================
        # Create products
        # ==========================

        for index, item in enumerate(products):

            product, _ = ProductModel.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "category": item["category"],
                    "description": item["description"],
                    "base_price": item["price"],
                    "is_active": True,
                },
            )

            color_options = list(colors.values()) if item["has_color"] else [None]

            size_options = list(sizes.values()) if item["has_size"] else [None]

            variant_count = 0

            for color in color_options:

                for size in size_options:

                    variant_count += 1

                    sku_parts = [f"P-{product.id.hex[:8]}"]

                    if color:
                        sku_parts.append(color.value[:2].upper())

                    if size:
                        sku_parts.append(size.value)

                    sku = "-".join(sku_parts)

                    variant, created = ProductVariantModel.objects.get_or_create(
                        product=product,
                        sku=sku,
                        defaults={
                            "stock": random.randint(
                                5,
                                50,
                            ),
                            "is_active": True,
                        },
                    )

                    if created:

                        values = [
                            value
                            for value in [
                                color,
                                size,
                            ]
                            if value
                        ]

                        variant.attribute_values.set(values)

            # ==========================
            # Image
            # ==========================

            if not product.images.exists():  # type: ignore

                image = make_placeholder_image(
                    f"product-{index}",
                    PALETTE[index % len(PALETTE)],
                )

                ProductImageModel.objects.create(
                    product=product,
                    image=image,
                    alt_text=product.name,
                    is_main=True,
                )

            self.stdout.write(
                self.style.SUCCESS(f"{product.name} -> {variant_count} variants")
            )

        self.stdout.write(self.style.SUCCESS("Seed data completed successfully."))
