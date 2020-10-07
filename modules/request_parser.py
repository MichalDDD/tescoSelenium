import requests
import bs4
import re

def get_response(url: str) -> bs4.BeautifulSoup:
    """
    method used to send a http request and return the response as a html tree
    :param url: url of the request
    :return bs4.BeautifulSoup: html tree of response content
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    return bs4.BeautifulSoup(response.content, 'html.parser')

def remove_imperial_units(string: str) -> str:
    """
    method used to split string containing both metric and imperial units
    :param string: string searched for e character
    :return str: part of the string before the e character
    """
    id_1 = string.rfind(' e')
    id_2 = string.rfind(' ℮')
    m = max(id_1, id_2)
    if m > -1:
        string = string[:m]
    return string

def split_units(unit_str: str) -> list:
    """
    method used to split net content string of a product into quantity and type of unit
    :param unit_str: net content string from product html file
    :return list: 2 element list where 0 is quantity and 1 is unit type
    """
    unit_str = unit_str.lower()
    unit_str = remove_imperial_units(unit_str)
    last_digit = re.match('.+([0-9])[^0-9]*$', unit_str)
    quantity = unit_str[:last_digit.start(1) + 1]
    unit_type = unit_str[last_digit.start(1) + 1:].replace(' ','')
    if quantity.rfind('count') > -1:
        quantity = 1
    if unit_type == '':
        unit_type = 'item'
    return [quantity, unit_type]

def extract_product_info(url: str) -> list:
    """
    method used to get product information using a http request and scraping it for product info
    :param url: url of a certain product on a website
    :return list: returns a 5 element list where:
    0 - product name,
    1 - product price,
    2 - currency,
    3 - product quantity
    4 - quantity unit type
    """
    soup = get_response(url)
    product_name = soup.find('h1', class_='product-details-tile__title').text
    price_wrapper = soup.find('div', class_='price-control-wrapper')
    try:
        price = price_wrapper.find('span', class_='value').text
        currency = price_wrapper.find('span', class_='currency').text
    except AttributeError:
        price = 'product is currently unavailable'
        currency = None
    try:
        contents = soup.find('div', id='net-contents').find('p', class_='product-info-block__content').text
        content_list = split_units(contents)
    except AttributeError:
        content_list = [1, 'item']

    return [product_name, price, currency, content_list[0], content_list[1]]
