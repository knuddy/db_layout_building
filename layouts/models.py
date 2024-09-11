from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Page(models.Model):
    class PageHeightChoices(models.TextChoices):
        CONTAIN = "Contain"
        GROW = "Grow"

    name = models.CharField(max_length=255, blank=False, null=False, help_text="What is the name of this view?")
    rows = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    columns = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    page_height = models.CharField(max_length=20, choices=PageHeightChoices.choices, default=PageHeightChoices.CONTAIN, blank=False, null=False)

    @property
    def total_capacity(self):
        return self.rows * self.columns


class PageObject(models.Model):
    page = models.ForeignKey(Page, blank=False, null=False, on_delete=models.CASCADE, related_name='page_objects')
    position = models.PositiveIntegerField(blank=False, null=False)
    row_span = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    column_span = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['page', 'position'], name='constraint_unique_page_position')
        ]
