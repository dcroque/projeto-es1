from terabyte_scrapper import *
class Menu:
    def __init__(self):
         pass

    def show_menu(self, tag):

         path = "pathtest/teste.html"
         url = url_search(tag)

         scr.get_html_file(url, path)
         html_info = scr.read_file(path)

         produtos = get_products(html_info)

         for item in produtos:
             if item.available and (item.name).find(tag) != -1:
                 item.print_info()
        

