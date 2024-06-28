from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# url = 'https://vkusnotochkamenu.ru/'
header = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36",
}
# req = requests.get(url, headers=header)
# src = req.text

# # сохраняем страницу в отдельный файл
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(src)

# # откроем-прочитаем файл, сохраним в отдельную переменную
# with open("index.html", encoding="utf-8") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")
# # получаем ссылки на категории
# all_products_hrefs = soup.find("ul", class_="nav navbar-nav").find_all("a")

# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = item.get("href")

#     all_categories_dict[item_text.strip()] = item_href
# # сохраняем в виде словаря {ключ(категория): значение(ссылка)} в json
# with open("all_categories_dict.json", "w", encoding='utf_8') as file:
#     json.dump(
#         all_categories_dict,
#         file,
#         indent=4,
#         ensure_ascii=False
#     )
# далее json открываем и будем по очереди из каждой ссылки вынимать информацию о каждом блюде
with open("all_categories_dict.json", encoding="utf-8") as file:
    all_categories = json.load(file)
count = 0
for category_name, category_href in all_categories.items():
    if count >= 0:
        req = requests.get(url=category_href, headers=header)
        src = req.text
        # сохраним в отдельный файл, информацию о каждом разделе с блюдами, в html
        with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
            file.write(src)
        # открываем файл для сбора информации о каждом отдельном блюде со страницы
        with open(f"data/{count}_{category_name}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_links = soup.find_all(
            "div",
            class_="product-layout product-grid col-lg-2 col-md-3 col-sm-4 col-xs-6 h285",
        )

        # собираем данные о каждом блюде
        data = []
        # try:except необходим, т.к. есть блюда где присутствует только название и цена. без него вылазит AttributeError
        for link in all_links:
            try:
                data.append(
                    {
                        "name": " ".join(
                            link.find("p", class_="line-height-20").text.split()[:-3]
                        ),
                        "price": " ".join(
                            link.find("p", class_="line-height-20").text.split()[-2:]
                        ),
                        "calories": link.find("i").text,
                        "PFC": link.find(class_="font_12 font-weight-600").text,
                    }
                )
            except AttributeError:
                data.append(
                    {
                        "name": " ".join(
                            link.find("p", class_="line-height-20").text.split()[:-3]
                        ),
                        "price": " ".join(
                            link.find("p", class_="line-height-20").text.split()[-2:]
                        ),
                    }
                )
        # Красиво и легко запишем сюда
        df = pd.DataFrame(data)
        # создается csv файл для каждой катеогрии по которой мы проходимся
        # параметр sep=';' для excel
        gfg_csv_data = df.to_csv(
            f"data/{count}_{category_name}.csv",
            sep=";",
            encoding="utf-8-sig",
            index=False,
        )

    count += 1
