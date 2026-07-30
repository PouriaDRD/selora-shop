from django import forms

from store.models import ProductVariantModel


class ProductVariantAdminForm(forms.ModelForm):

    class Meta:
        model = ProductVariantModel
        fields = "__all__"

    def clean_attribute_values(self):
        values = self.cleaned_data.get("attribute_values")

        if not values:
            return values

        attribute_ids = list(
            values.values_list(
                "attribute_id",
                flat=True,
            )
        )

        # هر attribute فقط یک value
        if len(attribute_ids) != len(set(attribute_ids)):
            raise forms.ValidationError("هر ویژگی فقط می‌تواند یک مقدار داشته باشد.")

        return values

    def clean(self):
        cleaned_data = super().clean()

        product = cleaned_data.get("product")
        attribute_values = cleaned_data.get("attribute_values")

        if not product or not attribute_values:
            return cleaned_data

        current_values = set(
            attribute_values.values_list(
                "id",
                flat=True,
            )
        )

        variants = (
            ProductVariantModel.objects.filter(product=product)
            .exclude(pk=self.instance.pk)
            .prefetch_related("attribute_values")
        )

        for variant in variants:

            variant_values = set(
                variant.attribute_values.values_list(
                    "id",
                    flat=True,
                )
            )

            if variant_values == current_values:
                raise forms.ValidationError(
                    "این ترکیب ویژگی قبلاً برای این محصول ساخته شده است."
                )

        return cleaned_data
