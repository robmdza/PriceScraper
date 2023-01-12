import requests
from bs4 import BeautifulSoup
import sqlite3


def save_to_database(title, price, shipping, condition, url):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
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
    url = "https://listado.mercadolibre.com.mx/computacion/" \
          "%22quest-2%22_" \
          "PriceRange_4000-7000_NoIndex_True#applied_filter_id%3Dcategory%26" \
          "applied_filter_name%3DCategor%C3%ADas%26applied_filter_order%3D4%26" \
          "applied_value_id%3DMLM1648%26applied_value_name%3DComputaci%C3%B3n%26" \
          "applied_value_order%3D2%26applied_value_results%3D4%26is_custom%3Dfalse"
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
                                 class_='andes-card andes-card--flat andes-card--default ui-search-result '
                                        'shops__cardStyles ui-search-result--core andes-card--padding-default')
    for element in all_elements:
        title = element.find('h2', class_="ui-search-item__title shops__item-title").text
        price = element.find('span', class_="price-tag-text-sr-only").text.replace(' pesos', '')
        url = element.find('a', class_="ui-search-item__group__element shops__items-group-details ui-search-link")['href']
        try:
            condition = element.find('span',
                                     class_='ui-search-item__group__element ui-search-item__details '
                                            'shops__items-group-details').text
        except:
            condition = 'none'
        try:
            shipping = element.find('p',
                                    class_="ui-search-item__shipping ui-search-item__shipping--free "
                                           "shops__item-shipping-free").text
        except:
            shipping = 'none'
        print(title, price, shipping, condition, url)
        save_to_database(title, price, shipping, condition, url)
        # print(element.get_text())


def start():
    page = execute_search()
    parse_data(page)
    # print(num[0])



