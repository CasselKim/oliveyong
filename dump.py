import os
import django
import random
import datetime
from decimal import Decimal
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from app.models import Brand, CategoryChoices, Product, Campaign, CostShare

fake = Faker('ko_KR')

Campaign.objects.all().delete()
CostShare.objects.all().delete()
Product.objects.all().delete()
Brand.objects.all().delete()

SEGMENT_RANK = {
    '"NO OLIVE"': 0,
    '"BABY OLIVE"': 1,
    '"PINK OLIVE"': 2,
    '"GREEN OLIVE"': 3,
    '"BLACK OLIVE"': 4,
    '"GOLD OLIVE"': 5
}


# # # 1. 브랜드 생성 (예: 30개)
brand_count = 30
brands = []
for i in range(brand_count):
    b = Brand.objects.create(name=f"Brand_{i+1}", description=fake.catch_phrase())
    brands.append(b)

# 2. 상품 30,000개 생성
products = []
for i in range(30000):
    brand = random.choice(brands)
    price = random.randint(5000, 100000)
    # 카테고리 등은 단순처리
    product = Product.objects.create(
        brand=brand,
        name=f"Product_{i+1}",
        description=fake.sentence(nb_words=12),
        price=price,
        category=random.choice(CategoryChoices.choices)[0],
        thumbnail=f"img/thumbnails/pokemon_{i%1000}.png"
    )
    products.append(product)

# 날짜 설정
today = datetime.date.today()
past_day = today - datetime.timedelta(days=30)  # 과거
future_day = today + datetime.timedelta(days=30) # 미래
valid_start = today - datetime.timedelta(days=1)
valid_end = today + datetime.timedelta(days=10)

# 유효하지 않은 캠페인 100개
# Case 1: 이미 끝난 캠페인 end_date < today
# Case 2: 아직 시작 안한 캠페인 start_date > today
invalid_campaigns = []
for i in range(100):
    # 무작위로 미래시작, 과거끝 둘 중 하나 선택
    if random.random() < 0.5:
        # 이미 끝난 캠페인
        start_date = past_day
        end_date = today - datetime.timedelta(days=random.randint(1,10))
    else:
        # 아직 시작 안함
        start_date = today + datetime.timedelta(days=random.randint(1,10))
        end_date = start_date + datetime.timedelta(days=5)

    c = Campaign.objects.create(
        name=f"Invalid_Campaign_{i+1}",
        start_date=start_date,
        end_date=end_date,
        discount_type=random.choice(['FIXED','RATE']),
        discount_value=random.randint(5,50),
        dsl=""  # DSL 비울 수도 있음
    )
    invalid_campaigns.append(c)

# 유효한 캠페인 300개
# 모두 다른 DSL, 다른 name, discount_type, discount_value, cost_shares

segments = ["BLACK OLIVE", "GREEN OLIVE", "PINK OLIVE", "BABY OLIVE", "NO OLIVE"]

def random_condition(cnt):
    """하나의 조건 문자열 생성 예: 'brand_id = 5', 'product_id IN [101,102]', 'mov > 50000', 'customer_segment = "VIP"'"""
    fields = random.sample(["brand_id", "product_id", "customer_segment", "mov", "category"], cnt)
    conditions = []
    for field in fields:
        if field == "brand_id":
            op = random.choice(["=", "IN"])
            if op == "IN":
                vals = random.sample(range(1, brand_count+1), k=random.randint(1,5))
                vals_str = ",".join(map(str, vals))
                conditions.append(f'brand_id IN [{vals_str}]')
            else:
                val = random.randint(1, brand_count)
                conditions.append(f"brand_id {op} {val}")
        elif field == "product_id":
            op = random.choice(["=", "IN"])
            if op == "IN":
                # IN에 최대 5개 랜덤 product_id
                vals = random.sample(range(1,30001), k=random.randint(1,3000))
                vals_str = ",".join(map(str, vals))
                conditions.append(f'product_id IN [{vals_str}]')
            else:
                val = random.randint(1,30000)
                conditions.append(f"product_id {op} {val}")
        elif field == "customer_segment":
            op = random.choice(["=", ">", "<", ">=", "<="])  # customer_segment는 비교 가능(등급으로), IN은 제외
            seg = random.choice(segments)
            conditions.append(f'customer_segment {op} "{seg}"')
        elif field == "category":
            op = random.choice(["=", "IN"])
            if op == "IN":
                vals = random.sample(range(1, len(CategoryChoices.choices)), k=random.randint(1,5))
                vals_str = ",".join(map(str, vals))
                conditions.append(f'category IN [{vals_str}]')
            else:
                val = random.randint(1, len(CategoryChoices.choices))
                conditions.append(f"category {op} {val}")
        else: # mov
            op = random.choice([">="])
            val = random.randint(0,100000)
            conditions.append(f"mov {op} {val}")
    return conditions
    
# def random_expression(depth=0):
#     # depth가 5에 도달하면 더 이상 재귀 깊이를 늘리지 않고 Leaf 조건으로 전환
#     # depth가 깊어질수록 Leaf를 선택할 확률을 높여도 됨
#     max_depth = 5
    
#     # Leaf 조건을 반환할지 결정
#     # 깊이가 깊어질수록 Leaf로 전환할 가능성 증가
#     # 예: depth가 높을수록 1에 가까운 확률로 leaf
#     leaf_probability = 0.2 * (depth + 1)
#     if depth >= max_depth or random.random() < leaf_probability:
#         # Leaf 조건 (단일 condition)
#         return random_condition()

#     # Leaf가 아니라면 1~3개의 sub-expression을 만든다.
#     sub_count = random.randint(1,3)
#     sub_expressions = [random_expression(depth+1) for _ in range(sub_count)]

#     if sub_count == 1:
#         # 하나의 서브 표현식만 있으면 괄호를 추가해 다양성 증가
#         # 꼭 괄호를 넣지 않아도 되나, 일관성을 위해 괄호 삽입
#         return f"({sub_expressions[0]})"
#     else:
#         # 2~3개의 서브 표현식을 AND/OR로 연결
#         expr = sub_expressions[0]
#         for c in sub_expressions[1:]:
#             op = random.choice(["AND"])
#             # 괄호를 적극적으로 사용
#             # 예: (expr AND c), (expr OR c) 형태로 감싸기
#             expr = f"({expr} {op} {c})"
#         return expr

# def random_dsl():
#     # random_expression(0)을 호출해 DSL 생성
#     # 최종적으로 나온 DSL이 곧 다양한 depth와 괄호를 포함
#     return random_expression(depth=0)


def random_dsl():
    # 조건 1~3개를 AND/OR로 연결
    cond_count = random.randint(1,5)
    conditions = " AND ".join(random_condition(cond_count))
    return conditions


valid_campaigns = []
seen_dsls = set()

for i in range(300):
    # 유효한 캠페인 날짜
    start_date = valid_start
    end_date = valid_end
    # DSL 유니크하게 생성
    cond_count = random.randint(1,5)
    conditions = random_condition(cond_count)
    dsl_str = " AND ".join(conditions)

    # 중복되면 다시 시도
    retries = 0
    while dsl_str in seen_dsls and retries < 50:
        dsl_str = random_dsl()
        retries += 1
    seen_dsls.add(dsl_str)

    # discount
    discount_type = random.choice(['FIXED','RATE'])
    discount_value = random.randint(5,50)

    brand_ids = []
    product_ids = []
    category_ids = []
    minimum_customer_segment = None
    minimum_mov = None

    for c in conditions:
        if c.startswith("brand_id"):
            if c.split(" ")[1] == "IN":
                brand_ids.extend(eval(" ".join(c.split(" ")[2:])))
            else:
                brand_ids.append(int(c.split(" ")[2]))
        elif c.startswith("product_id"):
            if c.split(" ")[1] == "IN":
                product_ids.extend(eval(" ".join(c.split(" ")[2:])))
            else:
                product_ids.append(int(c.split(" ")[2]))
        elif c.startswith("category"):
            if c.split(" ")[1] == "IN":
                category_ids.extend(eval(" ".join(c.split(" ")[2:])))
            else:
                category_ids.append(int(c.split(" ")[2]))
        elif c.startswith("customer_segment"):
            minimum_customer_segment = SEGMENT_RANK[" ".join(c.split(" ")[2:])]
        elif c.startswith("mov"):
            minimum_mov = int(c.split(" ")[2])

    # 캠페인 생성
    c = Campaign.objects.create(
        name=f"Valid_Campaign_{i+1}",
        start_date=start_date,
        end_date=end_date,
        discount_type=discount_type,
        discount_value=discount_value,
        dsl=dsl_str,
        brand_ids=brand_ids,
        product_ids=product_ids,
        category_ids=category_ids,
        minimum_customer_segment=minimum_customer_segment,
        minimum_mov=minimum_mov
    )
    valid_campaigns.append(c)

    # cost_shares 랜덤 0~3개
    share_count = random.randint(0,3)
    for sc in range(share_count):
        share_type = random.choice(['FIXED','RATE','RATIO'])
        share_val = random.randint(1,50)
        CostShare.objects.create(
            campaign=c,
            entity_name=f"Entity_{sc+1}",
            share_type=share_type,
            share_value=share_val
        )

print("Data generation completed!")
print(f"Brands: {brand_count}, Products: 30000, Invalid Campaigns: 100, Valid Campaigns: 300")