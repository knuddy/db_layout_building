from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Page(models.Model):
    class PageBounds(models.TextChoices):
        CONTAIN = "Contain"
        GROW = "Grow"

    name = models.CharField(max_length=255, blank=False, null=False, help_text="What is the name of this view?")
    bounds = models.CharField(max_length=20, choices=PageBounds.choices, default=PageBounds.CONTAIN, blank=False, null=False)
    columns = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    rows = models.IntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    fixed_row_size = models.IntegerField(validators=[MinValueValidator(1)], blank=True, null=True)

    def clean(self):
        if self.bounds == self.PageBounds.CONTAIN and self.rows is None:
            raise ValidationError("Rows must have a value when Page bounds is set to Contain")
        elif self.bounds == self.PageBounds.GROW and self.fixed_row_size is None:
            raise ValidationError("fixed_row_size must have a value when Page bounds is set to Grow")

    @property
    def total_capacity(self):
        return self.rows * self.columns

    @property
    def objects_list(self):
        return self.page_objects.all().order_by('position')

    def __str__(self):
        return self.name


class PageObject(models.Model):
    page = models.ForeignKey(Page, blank=False, null=False, on_delete=models.CASCADE, related_name='page_objects')
    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    row_span = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    column_span = models.IntegerField(default=1, validators=[MinValueValidator(1)])
