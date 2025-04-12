from django.db import models

from utils.DSL.evaluate import SEGMENT_RANK

class CategoryChoices(models.TextChoices):
    스킨케어 = '스킨케어', '스킨케어'
    마스크팩 = '마스크팩', '마스크팩'
    클렌징 = '클렌징', '클렌징'
    선케어 = '선케어', '선케어'
    메이크업 = '메이크업', '메이크업'
    네일 = '네일', '네일'
    뷰티소품 = '뷰티소품', '뷰티소품'
    더모코스메틱 = '더모 코스메틱', '더모 코스메틱'
    맨즈케어 = '맨즈케어', '맨즈케어'
    향수디퓨저 = '향수/디퓨저', '향수/디퓨저'
    헤어케어 = '헤어케어', '헤어케어'
    바디케어 = '바디케어', '바디케어'
    건강식품 = '건강식품', '건강식품'
    푸드 = '푸드', '푸드'
    구강용품 = '구강용품', '구강용품'
    헬스건강용품 = '헬스/건강용품', '헬스/건강용품'
    여성위생용품 = '여성/위생용품', '여성/위생용품'
    패션 = '패션', '패션'
    리빙가전 = '리빙/가전', '리빙/가전'
    취미펫용품 = '취미/펫용품', '취미/펫용품'

CATEGORY_ID = {
    '스킨케어': 1,
    '마스크팩': 2,
    '클렌징': 3,
    '선케어': 4,
    '메이크업': 5,
    '네일': 6,
    '뷰티소품': 7,
    '더모 코스메틱': 8,
    '맨즈케어': 9,
    '향수/디퓨저': 10,
    '헤어케어': 11,
    '바디케어': 12,
    '건강식품': 13,
    '푸드': 14,
    '구강용품': 15,
    '헬스/건강용품': 16,
    '여성/위생용품': 17,
    '패션': 18,
    '리빙/가전': 19,
    '취미/펫용품': 20
}

class Brand(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.RESTRICT, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(null=False)
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
    )
    thumbnail = models.CharField(max_length=200, blank=True, null=True)
    

class Campaign(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('FIXED', '정액 할인'),
        ('RATE', '정률 할인')
    ]

    name = models.CharField(max_length=100, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    discount_type = models.CharField(max_length=5, choices=DISCOUNT_TYPE_CHOICES, default='RATE')
    discount_value = models.IntegerField(null=False)
    brand_ids = models.JSONField(default=list)
    product_ids = models.JSONField(default=list)
    category_ids = models.JSONField(default=list)
    minimum_customer_segment = models.IntegerField(null=True)
    minimum_mov = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
class CostShare(models.Model):
    SHARE_TYPE_CHOICES = [
        ('FIXED', '정액 분담'),
        ('RATE', '정률 분담'),
        ('RATIO', '비율 분담')
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='cost_shares')
    entity_name = models.CharField(max_length=100)
    share_type = models.CharField(max_length=5, choices=SHARE_TYPE_CHOICES)
    share_value = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.entity_name} - {self.share_type} {self.share_value}"