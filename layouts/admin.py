from django.contrib import admin
from django import forms
from layouts.models import Page, PageObject


class PageObjectInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()

        if not self.forms:
            return

        parent: Page = self.forms[0].cleaned_data['page']
        total_space_used = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                continue
            data = form.cleaned_data
            total_space_used += data['row_span'] * data['column_span']

        if total_space_used > parent.total_capacity:
            raise forms.ValidationError("Not enough rows and columns to fit these objects!")


class PageObjectInline(admin.TabularInline):
    formset = PageObjectInlineFormset
    model = PageObject
    extra = 0
    ordering = ['position']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': (('name', 'slug'),)}),
        ('Layout', {'fields': (('bounds', 'columns', 'rows', 'content_spacing'),)}),
        ('Extras for use when Bounds is Grow', {'fields': (('row_size', 'row_unit'),)}),
    )
    inlines = [PageObjectInline]
