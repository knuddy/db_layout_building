from django.contrib import admin
from django import forms
from layouts.models import PageObject, Page


class PageObjectInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if not self.forms:
            return

        parent: Page = self.forms[0].cleaned_data['page']
        total_space_used = 0
        for form in self.forms:
            if not form.cleaned_data:
                continue
            data = form.cleaned_data
            total_space_used += data['row_span'] * data['column_span']

        if total_space_used > parent.total_capacity:
            raise forms.ValidationError("Too many rows and columns used!")


class PageObjectInline(admin.TabularInline):
    formset = PageObjectInlineFormset
    model = PageObject
    extra = 0
    ordering = ['position']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ('name', )}),
        ('Layout', {'fields': ('bounds', 'columns')}),
        ('Only Relevant When BOUNDS = CONTAIN', {'fields': ('rows',)}),
        ('Only Relevant When BOUNDS = GROW', {'fields': ('fixed_row_size', )}),
    )
    inlines = [PageObjectInline]