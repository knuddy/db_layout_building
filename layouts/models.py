from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Page(models.Model):
    class PageBounds(models.TextChoices):
        CONTAIN = "Contain"
        GROW = "Grow"

    class RowUnit(models.TextChoices):
        PX = ("px", "Pixels")
        FRACTION = ("fr", "Fraction Of Page Height")

    name = models.CharField(max_length=255, blank=False, null=False, help_text="What is the name of this page?")
    slug = models.SlugField(blank=False, null=False, unique=True)
    bounds = models.CharField(max_length=20, choices=PageBounds.choices, default=PageBounds.CONTAIN, blank=False, null=False)
    columns = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    content_spacing = models.FloatField(default=0.5, validators=[MinValueValidator(0.0)], blank=False, null=False, help_text="Spacing between objects. Unit is in REM")
    rows = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    row_size = models.IntegerField(default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    row_unit = models.CharField(max_length=5, choices=RowUnit.choices, default=RowUnit.PX, blank=True, null=True)

    @property
    def total_capacity(self):
        return self.rows * self.columns

    @property
    def objects_list(self):
        return self.page_objects.all().order_by('position')

    def css_grid_template_row_value(self):
        value = "1fr"
        if self.bounds == Page.PageBounds.GROW:
            if self.row_unit == Page.RowUnit.FRACTION:
                value = f"calc((100% / {self.row_size}) - ({self.row_size - 1} * var(--content-padding) / {self.row_size}))"
            else:
                value = "%s%s" % (self.row_size, self.row_unit)
        return "repeat(%s, %s)" % (self.rows, value)

    def clean(self):
        if self.bounds == Page.PageBounds.GROW:
            if self.row_size is None:
                raise ValidationError("row_size must have a value when Page bounds is set to Grow")
            if self.row_unit is None:
                raise ValidationError("row_unit must have a value when Page bounds is set to Grow")

    def __str__(self):
        return self.name


class PageObject(models.Model):
    page = models.ForeignKey(Page, blank=False, null=False, on_delete=models.CASCADE, related_name='page_objects')
    position = models.PositiveIntegerField(blank=False, null=False)
    row_span = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    column_span = models.IntegerField(default=1, validators=[MinValueValidator(1)])
