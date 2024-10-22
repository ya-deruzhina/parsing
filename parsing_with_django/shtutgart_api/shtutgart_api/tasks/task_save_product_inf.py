from shtutgart_api.celery import app
from apps.wb.models import *
from apps.wb.serializers import *
import requests
from apps.wb.servise import servise_chose_data_product


@app.task()
def save_product_inf_task (id_product):
    headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
                'Accept': '*/*',
                'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
                # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Origin': 'https://www.wildberries.ru',
                'Connection': 'keep-alive',
                'Referer': 'https://www.wildberries.ru/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
            }
    id_product = str(id_product)

    numbers = ['01','02','03','04','05','06','07','08','09'] 
    for num in range(10,100):
        numbers.append(num)
    for i in numbers:
        try:
            url_data = f'https://basket-{i}.wbbasket.ru/vol{id_product[:4]}/part{id_product[:6]}/{id_product}/info/ru/card.json'
            product_info = requests.get(url_data,headers=headers).json()

            url_price = f'https://basket-{i}.wbbasket.ru/vol{id_product[:4]}/part{id_product[:6]}/{id_product}/info/price-history.json'
            data_price = requests.get(url_price,headers=headers).json()
        
        except:
            try:
                url_data = f'https://basket-{i}.wbbasket.ru/vol{id_product[:3]}/part{id_product[:5]}/{id_product}/info/ru/card.json'
                product_info = requests.get(url_data,headers=headers).json()

                url_price = f'https://basket-{i}.wbbasket.ru/vol{id_product[:3]}/part{id_product[:5]}/{id_product}/info/price-history.json'
                data_price = requests.get(url_price,headers=headers).json()
            
            except:
                try:
                    url_data = f'https://basket-{i}.wbbasket.ru/vol{id_product[:2]}/part{id_product[:4]}/{id_product}/info/ru/card.json'
                    product_info = requests.get(url_data,headers=headers).json()

                    url_price = f'https://basket-{i}.wbbasket.ru/vol{id_product[:2]}/part{id_product[:4]}/{id_product}/info/price-history.json'
                    data_price = requests.get(url_price,headers=headers).json()
                
                except:
                    continue
                else:
                    data = servise_chose_data_product(product_info,data_price,id_product)
                    if data:
                        break

            else:
                data = servise_chose_data_product(product_info,data_price,id_product)
                if data:
                    break

        else:
            data = servise_chose_data_product(product_info,data_price,id_product)
            if data:
                break


