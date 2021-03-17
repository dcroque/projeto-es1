import scrapper as scr
from classes import *

def load_main_page():
    text = scr.read_file("index.html")
    if text == '':
        scr.get_html_file("https://www.terabyteshop.com.br", "index.html")
        return scr.read_file("index.html")
    else:
        return text

def check_page_exist(url):
    #li class="icon-right categoria"
    text = load_main_page()
    categories = scr.get_all_html_elements(text, "li", 'class="icon-right categoria"')
    for element in categories:
        temp = element.find(url)
        if temp != -1:
            return True
    return False

def url_search(tags):
    tags = tags.replace(" ", "+")
    tags = tags.lower()
    return "https://www.terabyteshop.com.br/busca?str="+tags

def url_category(category):
    layer = 0
    url = "https://www.terabyteshop.com.br"
    url += "/"+category
    if check_page_exist(url):
        return url
    else:
        raise Exception("invalid url: " + url)

def get_products(text):
    return_array = []
    products_html = scr.get_all_html_elements(text, "div", 'class="pbox col-xs-12 col-sm-6 col-md-3"')
    for product in products_html:
        product_info = ['']*8
        product_info[0] = scr.get_element_complement(product, "a", "title")
        if product.find("Todos vendidos") != -1:
            info = [product_info[0], '', '', '', '', '', False, False]
        else:
            product_info[6] = True
            temp = scr.get_html_element(product, 'div', 'class="prod-old-price"')
            if temp == '':
                product_info[1] = ''
                temp = scr.get_html_element(product, 'div', 'class="prod-new-price"')
                product_info[2] = scr.get_html_element(temp, 'span')
                product_info[7] = False
            else:
                product_info[2] = scr.get_html_element(temp, 'span')
                temp = scr.get_html_element(product, 'div', 'class="prod-new-price"')
                product_info[1] = scr.get_html_element(temp, 'span')
                product_info[7] = True
            temp = scr.get_html_element(product, 'div', 'class="prod-juros"')
            temp = scr.get_all_html_elements(temp, "span")
            product_info[5] = temp[0][:len(temp[0])-1]
            product_info[4] = temp[1]
        temp = Product()
        temp.set_all(product_info)
        return_array.append(temp)
    return return_array

