from locust import HttpUser, task, between
from random import randint

class MyUser(HttpUser):
    wait_time = between(1, 5)  # 요청 사이에 1~5초의 대기시간
    
    @task
    def product_list(self):
        self.client.get(f"/products/?segment=BABY+OLIVE&page={randint(1, 626)}")  # /products 경로로 GET 요청
