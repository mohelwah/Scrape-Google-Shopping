import requests, json
from bs4 import BeautifulSoup
from outputs import output_json
import re

# CONFIGURATION
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
query = "lenovo thinkpad"
params = {"q": query, "hl": "en", 'gl': 'us', 'tbm': 'shop'}
freeDelivery = False
url = 'https://www.google.com/search'

# REQUEST
response = requests.get(url,
                        params=params,
                        headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

# PARSING RESPONSE
shopping_data_dict = {}
inline_results = []
shopping_results = []

for inline_result in soup.select('.sh-np__click-target'):
    inline_shopping_title = inline_result.select_one('.sh-np__product-title').text
    inline_shopping_link = f"https://google.com{inline_result['href']}"
    inline_shopping_price = inline_result.select_one('b').text
    inline_shopping_source = inline_result.select_one('.E5ocAb').text.strip()
    try:
      inline_shopping_shipping = inline_result.select_one('.U6puSd').text.strip()
    except:
      inline_shopping_shipping = None
      

    inline_results.append({
        'title': inline_shopping_title,
        'link': inline_shopping_link,
        'price': inline_shopping_price,
        'source': inline_shopping_source,
        'shipping': inline_shopping_shipping
    })

shopping_data_dict.update({"inline_shopping_results": inline_results})

for shopping_result in soup.select('.sh-dgr__content'):
    title = shopping_result.select_one('.Lq5OHe.eaGTj h4').text
    product_link = f"https://www.google.com{shopping_result.select_one('.Lq5OHe.eaGTj')['href']}"
    source = shopping_result.select_one('.IuHnof').text
    price = shopping_result.select_one('span.kHxwFf span').text

    try:
        rating = shopping_result.select_one('.Rsc7Yb').text
    except:
        rating = None

    try:
        reviews = shopping_result.select_one('.Rsc7Yb').next_sibling.next_sibling
    except:
        reviews = None

    try:
        delivery = shopping_result.select_one('.vEjMR').text
    except:
        delivery = None



    shopping_results.append({
    
            'title': title,
        'link': product_link,
        'source': source,
        'price': price,
        'rating': rating,
        'reviews': reviews,
        'delivery': delivery,
        'titke': f
    })

shopping_data_dict.update({"shopping_results": shopping_results})

output_json(shopping_data_dict, f'{params["q"]}{" with free delivery" if freeDelivery else ""}')

print("Done!")