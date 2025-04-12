import os
import django
import random
from decimal import Decimal
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')  # 프로젝트명.main.settings로 변경
django.setup()

from app.models import Brand, Product, CategoryChoices

fake = Faker('ko_KR')

# 브랜드 10개 생성
brand_names = [fake.company() for _ in range(10)]
brands = []
for name in brand_names:
    b = Brand.objects.create(name=name, description=fake.catch_phrase())
    brands.append(b)

categories = [c.value for c in CategoryChoices]  # CategoryChoices에 정의된 모든 카테고리 값 추출

# 각 카테고리별로 제품 100개씩 생성
# 카테고리 수 * 100개 제품
for cat in categories:
    for i in range(100):
        brand = random.choice(brands)
        product_name = f"[2024 어워즈]{fake.word()} {cat} {fake.color_name()}"
        price = Decimal(random.randint(5000, 100000))  # 5,000원~100,000원 사이 랜덤
        description = fake.sentence(nb_words=12)
        Product.objects.create(
            brand=brand,
            name=product_name,
            description=description,
            price=price,
            category=cat
        )

print("더미 데이터 생성 완료!")
