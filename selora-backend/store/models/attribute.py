import uuid
from django.db import models


class AttributeModel(models.Model):
    """
    A variant dimension, e.g. 'Color' or 'Size'.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"

    def __str__(self):
        return self.name


class AttributeValueModel(models.Model):
    """
    A concrete value of an attribute, e.g. 'Red' for 'Color'.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    attribute = models.ForeignKey(
        AttributeModel, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=60)

    class Meta:
        unique_together = ("attribute", "value")
        ordering = ["attribute__name", "value"]

        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
