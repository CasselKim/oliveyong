from django import forms
from django.contrib import admin

from utils.DSL.evaluate import SEGMENT_RANK
from .models import Brand, Campaign, CostShare, Product

class CostShareInline(admin.TabularInline):
    model = CostShare
    extra = 1

class CampaignAdminForm(forms.ModelForm):
    brand_ids = forms.CharField(required=False)
    product_ids = forms.CharField(required=False)
    category_ids = forms.CharField(required=False)
    minimum_mov = forms.DecimalField(required=False)
    minimum_customer_segment = forms.CharField(required=False)
    

    class Meta:
        model = Campaign
        fields = ['name', 'start_date', 'end_date', 'discount_type', 'discount_value', 'brand_ids', 'product_ids', 'category_ids', 'minimum_customer_segment', 'minimum_mov']

class CampaignAdmin(admin.ModelAdmin):
    form = CampaignAdminForm
    inlines = [CostShareInline]
    change_form_template = "admin/app/campaign/change_form.html"

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CostShare)
admin.site.register(Brand)
admin.site.register(Product)
