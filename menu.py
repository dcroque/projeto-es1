from terabyte_scrapper import *

class Menu:
    def __init__(self):
         self.options = [
             ["Nova compra", self.opt_new_cart],
             ["Carregar compra", self.opt_load_cart],
             ["Procurar", self.opt_search],
             ["Exit", self.opt_exit]
         ]

    def main_menu(self):
        while True:
            for i in range(len(self.options)):
                print(f"{i+1}: {self.options[i][0]}")
            choice = input("\nChoose an option: ")
            try:
                choice = int(choice)
                choice -= 1
                is_numerical = True
            except:
                is_numerical = False

            function_loaded = False
            if is_numerical:
                if choice >= 0 and choice < len(self.options):
                    selected_opt = self.options[choice][1]
                    function_loaded = True
                else:
                    print(f"Invalid option: Expected number choice between 1 and {len(self.options)}\n")
            else:
                for opt in self.options:
                    if choice == opt[0]:
                        selected_opt = opt[1]
                        function_loaded = True
                        break
                if not function_loaded:
                    print(f"Invalid option: Couldn't find an option named {choice}\n")
            
            if function_loaded:
                selected_opt()

    def opt_exit(self):
        exit()

    def opt_search(self):
        print(f"Opcao {3} nao implementado ainda")

    def opt_new_cart(self):
        print(f"Opcao {1} nao implementado ainda")

    def opt_load_cart(self):
        print(f"Opcao {2} nao implementado ainda")

    def show_menu(self, tag):

         path = "pathtest/teste.html"
         url = url_search(tag)

         scr.get_html_file(url, path)
         html_info = scr.read_file(path)

         produtos = get_products(html_info)

         for item in produtos:
             if item.available and (item.name).find(tag) != -1:
                 item.print_info()
        

