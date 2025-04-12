from django import template

register = template.Library()

@register.filter
def get_brand_name(brands, selected_brand):
    # brands는 Brand의 쿼리셋 혹은 리스트
    # selected_brand는 선택된 브랜드의 ID
    for b in brands:
        if str(b.id) == str(selected_brand):
            return b.name
    return "Unknown Brand"