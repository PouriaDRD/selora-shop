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

        if len(attribute_ids) != len(set(attribute_ids)):

            raise forms.ValidationError("Each attribute can only have one value")

        return values

    def clean(self):

        cleaned_data = super().clean()

        product = cleaned_data.get("product")

        values = cleaned_data.get("attribute_values")

        if not product or not values:
            return cleaned_data

        current_values = set(
            values.values_list(
                "id",
                flat=True,
            )
        )

        variants = (
            ProductVariantModel.objects.filter(
                product=product,
            )
            .exclude(
                pk=self.instance.pk,
            )
            .prefetch_related(
                "attribute_values",
            )
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
                    "This combination of attributes already exists.",
                )

        return cleaned_data
