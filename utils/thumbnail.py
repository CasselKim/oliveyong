import requests

for i in range(1026, 100*20+1):  # 1부터 100번 포켓몬까지
    url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
    res = requests.get(url).json()
    # 스프라이트 이미지 URL
    img_url = res['sprites']['front_default']
    if img_url:
        img_data = requests.get(img_url).content
        with open(f"static/img/thumbnails/pokemon_{i}.png", 'wb') as f:
            f.write(img_data)