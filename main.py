from modules.request_parser import get_response, extract_product_info
from modules.link_downloader import LinkDownloader
from modules.excel_writer import Writer
import pandas as pd

# initialize firefox browser and get links for chosen product categories
ld: LinkDownloader = LinkDownloader(['Bakery','Cereals','Fresh Food'])
links: dict = ld.get_links()
del ld

# preparing output dataframe
COLUMN_NAMES = ['Product Category', 'Product Title', 'Product URL', 'Product Price', 'Currency', 'Product Size', 'Product Unit']
product_df = pd.DataFrame(columns=COLUMN_NAMES)

# retrieving items from chosen category pages, getting product details and appending them into result dataframe
for key, value in links.items():
    if value != 0:
        value = value.replace('?include-children=true','')
        for i in range(1, 5):
            soup = get_response(value + '?page=' + str(i))
            items = soup.find_all('li', class_='product-list--list-item')
            for item in items:
                href = item.find('a')['href']
                product_link = 'https://www.tesco.com' + href
                product_info_list = extract_product_info(product_link)
                new_row = {
                    'Product Category': key,
                    'Product Title': product_info_list[0],
                    'Product URL': product_link,
                    'Product Price': product_info_list[1],
                    'Currency': product_info_list[2],
                    'Product Size': product_info_list[3],
                    'Product Unit': product_info_list[4]
                }
                product_df = product_df.append(new_row, ignore_index=True)

# inserting result df into excel file and formatting
writer = Writer(product_df, 'results.xlsx')
writer.format_and_save_to_xlsx()
