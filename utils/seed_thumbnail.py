# 예: seed_thumbnails.py (manage.py와 동일 디렉토리에)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from app.models import Product

# product의 총 개수를 가져와서 각 product에 맞는 썸네일 이름을 할당
# 예를 들어 pokemon_1.png, pokemon_2.png 순서대로
products = Product.objects.all().order_by('id')

i = 1
for p in products:
    filename = f"pokemon_{i%1000}.png"
    p.thumbnail = f"img/thumbnails/{filename}"
    p.save()
    i += 1

print("썸네일 매핑 완료!")