import requests
from bs4 import BeautifulSoup
import sqlite3
import configparser
import re


def save_to_database(title, price, shipping, condition, url):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print("---->" + title + price + shipping + condition + url)
    # Create a table to store the data
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        price REAL,
                        shipping INTEGER,
                        condition TEXT,
                        url TEXT)''')
    # Insert the data into the table
    cursor.execute('INSERT INTO items (title, price, shipping, condition, url) VALUES (?, ?, ?, ?, ?)',
                   (title, price, shipping, condition, url))
    conn.commit()
    # Close the connection to the database
    conn.close()


def execute_search():
    '''url = "https://listado.mercadolibre.com.mx/computacion/" \
          "%22quest-2%22_" \
          "PriceRange_4000-7000_NoIndex_True#applied_filter_id%3Dcategory%26" \
          "applied_filter_name%3DCategor%C3%ADas%26applied_filter_order%3D4%26" \
          "applied_value_id%3DMLM1648%26applied_value_name%3DComputaci%C3%B3n%26" \
          "applied_value_order%3D2%26applied_value_results%3D4%26is_custom%3Dfalse"'''

    config_obj = configparser.ConfigParser()
    config_obj.read('search.properties')
    category = config_obj.get('search_properties', 'category')
    product = config_obj.get('search_properties', 'product')
    price_low = config_obj.get('search_properties', 'price_low')
    price_top = config_obj.get('search_properties', 'price_top')

    url = f"https://listado.mercadolibre.com.mx/{product}_" \
          f"PriceRange_{price_low}-{price_top}_NoIndex_True#applied_filter_id%3Dprice" \
          f'%26applied_filter_name%3DPrecio%26applied_filter_order%3D13%26applied_value_id%3D{price_low}-{price_top}' \
          f'%26applied_value_name%3D{price_low}-{price_top}%26applied_value_order%3D4%26' \
          f'applied_value_results%3DUNKNOWN_RESULTS' \
          '%26is_custom%3Dfalse'

    response = requests.get(url)
    if response.status_code == 200:
        with open('page.html', 'w') as f:
            f.write(response.text)
            return response.text
    else:
        print('Request Failed')
        return "Failed"
# print(response.ok)


def parse_data(response):
    soup = BeautifulSoup(response, "html.parser")
    num_results_element = soup.find('span',
                                    class_='ui-search-search-result__quantity-results shops-custom-secondary-font')
    num_results = num_results_element \
        .get_text()
    num = num_results.split(' ')

    # Get All the items from the results page
    all_items = soup.find_all('h2', class_='ui-search-item__title shops__item-title')
    for item in all_items:
        print(item.get_text())

    all_elements = soup.find_all('div',
                                 class_='ui-search-result__content-wrapper shops__result-content-wrapper')
    print("All: ",  len(all_elements))

    for element in all_elements:
        title = element.find('h2', class_="ui-search-item__title shops__item-title").text
        price = element.find('span', class_="andes-visually-hidden").text.replace(' pesos', '')
        url = element.find('a', class_="ui-search-item__group__element shops__items-group-details ui-search-link")['href']
        try:
            condition = element.find('span',
                                     class_='ui-search-item__group__element ui-search-item__details shops__'
                                            'items-group-details').text
        except:
            condition = 'none'
        try:
            shipping = element.find('p', class_="ui-meliplus-pill meliplus--actived ui-pb-label-builder "
                                                "ui-meliplus-pill meliplus--actived meli_plus").text
        except:
            shipping = 'none'

        config_obj = configparser.ConfigParser()
        config_obj.read('search.properties')
        product = config_obj.get('search_properties', 'product')
        product_keyword = config_obj.get('search_properties', 'product_keyword')

        pattern_product = re.escape(product.replace("-", " "))
        if product_keyword != "":
            pattern_keyword = re.escape(product_keyword.replace("-", " "))
        else:
            pattern_keyword = r'.+'

        print(pattern_product, pattern_keyword)
        title_exact_match = re.search(pattern_product, title, re.IGNORECASE)
        title_has_keyword = re.search(pattern_keyword, title, re.IGNORECASE)
        if bool(title_exact_match) and bool(title_has_keyword):
            title_matches = True
        else:
            title_matches = False

        if title_matches:
            save_to_database(title, price, shipping, condition, url)
            print("Saving to Database =================")
            print(title, price, shipping, condition, url)
        # print(element.get_text())


def clear_sqlite_database(database_name):
    try:
        # Connect to the database
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Get a list of tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Clear data from each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"Cleared data from table: {table_name}")

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print("Database cleared successfully.")
    except sqlite3.Error as e:
        print("Error:", e)


def start():
    clear_sqlite_database('database.db')
    page = execute_search()
    parse_data(page)
    # print(num[0])



