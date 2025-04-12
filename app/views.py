from decimal import Decimal
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from app.models import CATEGORY_ID, Campaign, Product, CategoryChoices, Brand
from lark import Lark
from utils.DSL.transformer import ConditionTransformer
from utils.DSL.evaluate import SEGMENT_RANK, evaluate_condition
import json
import logging
import sys
from django.db.models import Q

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def product_list(request):
    # segment 값 처리
    segment_param = request.GET.get('segment')
    if segment_param:
        request.session['customer_segment'] = segment_param
    customer_segment = request.session.get('customer_segment', 'UNSCRIBED')

    # brand 값 처리
    brand_param = request.GET.get('brand', '')  # ''이면 전체
    selected_brand = brand_param if brand_param else None

    categories = [c.value for c in CategoryChoices]
    selected_category = request.GET.get('category', '')

    page_size = 48
    page_number = int(request.GET.get('page', 1))

    base_query = Product.objects.all()
    if selected_category:
        base_query = base_query.filter(category=selected_category)
    if selected_brand:
        base_query = base_query.filter(brand_id=selected_brand)

    paginator = Paginator(base_query, page_size)
    page_obj = paginator.get_page(page_number)

    product_list = []
    today = timezone.now().date()

    # DSL 파서
    with open('utils/DSL/grammer.lark', 'r', encoding='utf-8') as f:
        condition_grammar = f.read()
    parser = Lark(condition_grammar, start='start', parser='lalr', transformer=ConditionTransformer())

    valid_campaigns = Campaign.objects.filter(
        start_date__lte=today,
        end_date__gte=today,
    )

    for p in page_obj.object_list:
        sale_price = p.price
        has_campaign = False
        tags = []

        for campaign in valid_campaigns:
            # if campaign.minimum_customer_segment and SEGMENT_RANK[customer_segment] < campaign.minimum_customer_segment:
            #     continue
            # if campaign.minimum_mov and p.price < campaign.minimum_mov:
            #     continue
            # if p.id not in campaign.product_ids:
            #     continue
            # if p.brand_id not in campaign.brand_ids:
            #     continue
            # if CATEGORY_ID[p.category] not in campaign.category_ids:
            #     continue
            
            if campaign.dsl:
                context = {
                    "brand_id": p.brand_id,
                    "product_id": p.id,
                    "customer_segment": customer_segment,
                    "mov": p.price,
                    "category_id": CATEGORY_ID[p.category],
                }

                try:
                    condition_tree = parser.parse(campaign.dsl)
                    condition_result = evaluate_condition(condition_tree, context)
                except Exception as e:
                    condition_result = False
                    logger.error(e)

                if condition_result:
                    # 할인액 계산
                    if campaign.discount_type == 'FIXED':
                        final_discount = campaign.discount_value
                    else: # RATE
                        final_discount = p.price * (campaign.discount_value / 100)

                    # 분담 계산 (실제 금액 계산은 여기서 필요할 경우 로깅 용도)
                    # 적용 예:
                    # FIXED 할인 + RATIO 분담일 경우:
                    # for cshare in campaign.cost_shares.all():
                    #   if cshare.share_type == 'RATIO':
                    #       entity_amount = final_discount * (cshare.share_value / 100)
                    #   elif cshare.share_type == 'FIXED':
                    #       entity_amount = cshare.share_value # 단, 사전에 합 검증 필요
                    #   # RATE 분담은 정률 할인일 때만 사용
                    #
                    # 여기서는 단순히 final_discount만 가격에 반영
                    # 실제 entity_amount 계산 및 상세 로직은 필요 시 로깅하거나 결과 저장 가능

                    sale_price -= final_discount
                    has_campaign = True
                    tags = ["세일"]
                    break


            # if campaign.discount_type == 'FIXED':
            #     final_discount = campaign.discount_value
            # else: # RATE
            #     final_discount = p.price * (campaign.discount_value / 100)

            # sale_price -= final_discount
            # has_campaign = True
            # tags = ["세일"]
            # break

        product_list.append({
            'id': p.id,
            'brand': p.brand.name,
            'name': p.name,
            'price': p.price,
            'has_campaign': has_campaign,
            'sale_price': sale_price,
            'tags': tags,
            'thumbnail': p.thumbnail
        })

    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = current_page - 2
    end_page = current_page + 2

    if start_page < 1:
        end_page += (1 - start_page)
        start_page = 1
    if end_page > total_pages:
        start_page -= (end_page - total_pages)
        end_page = total_pages
    if start_page < 1:
        start_page = 1

    page_range_display = range(start_page, end_page + 1)

    # brand 목록 로딩
    brands = Brand.objects.all().order_by('name')

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "products": product_list,
        "page_obj": page_obj,
        "page_range_display": page_range_display,
        "current_segment": customer_segment,
        "brands": brands,
        "selected_brand": selected_brand
    }

    return render(request, "product_list.html", context)