from terabyte_scrapper import *
from classes import *
from os import walk

class UserInterface:
    def __init__(self):
         self.options = [
             ["Nova compra", self.__opt_new_cart],
             ["Carregar compra", self.__opt_load_cart],
             ["Procurar", self.__opt_search],
             ["Sair", self.__opt_exit]
         ]

    def __menu_option_selection(self, label, options):
        while True:
            print(f"\n===== {label} =====\n")
            for i in range(len(options)):
                print(f"{i+1}: {options[i]}")
            choice = input("\nChoose an option: ")
            print()
            try:
                choice = int(choice)
                choice -= 1
                is_numerical = True
            except:
                is_numerical = False

            function_loaded = False
            if is_numerical:
                if choice >= 0 and choice < len(options):
                    function_loaded = True
                else:
                    print(f"Invalid option: Expected number choice between 1 and {len(options)}\n")
            else:
                for i in range(len(options)):
                    if choice == options[i]:
                        choice = i
                        break
                if not function_loaded:
                    print(f"Invalid option: Couldn't find an option named {choice}\n")

            if function_loaded:
                return choice

    def main_menu(self):
        main_options = [item[0] for item in self.options]
        while True:
            opt = self.__menu_option_selection("MENU PRINCIPAL", main_options)
            self.options[opt][1]()

    def __opt_exit(self):
        exit()

    def __opt_search(self, return_results=False):
        options = [
            "Pesquisar por nome",
            "Selecionar categoria",
            "Adicionar termos para filtrar",
            "Limpar filtros",
            "Sair"
        ]

        categories = [
            "Processador",
            "Placa de vídeo",
            "Placa mãe",
            "Memoria DDR4",
            "HD SATA III",
            "SSD",
            "Fontes",
            "Gabinetes",
            "Water Cooler"
            "Cooler CPU",
            "Cooler Gabinete"
        ]

        categories_dict = {
            "Processador": "hardware/processadores",
            "Placa de vídeo": "hardware/placas-de-video",
            "Placa mãe": "hardware/placas-mae",
            "Memoria DDR4": "hardware/memorias/ddr4",
            "HD SATA III": "hardware/hard-disk/hd-sata-iii",
            "SSD": "hardware/hard-disk/ssd",
            "Fontes": "hardware/fontes",
            "Gabinetes": "gabinetes",
            "Water Cooler": "refrigeracao/watercooler", 
            "Cooler CPU": "refrigeracao/cooler-p-cpu",
            "Cooler Gabinete": "refrigeracao/cooler-p-gabinete"
        }

        include_filters = []
        exclude_filters = []
        cat = ""

        while True:
            opt = self.__menu_option_selection("PROCURAR PRODUTO", options)

            if opt == 0:
                print("Insira que produto deseja pesquisar")
                if cat != "":
                    print(f"Categoria: {cat}")
                if len(exclude_filters):
                    print(f"Palavras filtradas: {exclude_filters}")
                include_filters = input().split()
                print()
                results = self.__func_search(cat, include_filters, exclude_filters)
                if not len(results):
                    print(f"Parece que nada foi encontrado com as palavras {include_filters} :(")
                else:
                    if return_results:
                        return results
                    for item in results:
                        item.print_info()

            elif opt == 1:
                cat = self.__menu_option_selection("SELECIONE A CATEGORIA", categories)
                cat = categories_dict[categories[cat]]

            elif opt == 2:
                print("Adicione palavras que necessariamente não aparecem no título do produto. Caso não queira adicionar nenhuma apenas aperte Enter.")
                if len(exclude_filters):
                    print(f"Palavras filtradas já incluídas: {exclude_filters}")
                new_exclude = input().split()
                if new_exclude != "":
                    for element in new_exclude:
                        exclude_filters.append(element)
            
            elif opt == 3:
                include_filters = []
                exclude_filters = []
                cat = ""
                print("Filtros limpos!")

            elif opt == 4:
                if return_results:
                    return []
                return
                
    def __opt_new_cart(self):
        shcart = ShoppingCart()
        #Carrinho vazio
        self.__func_shopping_cart(shcart)

    def __opt_load_cart(self):
        shcart = ShoppingCart()

        _, _, savefiles = next(walk("data/shoppingcarts"))
        options = []
        for item in savefiles:
            options.insert(0, str(item)[:-5])
        options.append("Sair")
        opt = self.__menu_option_selection("SELECIONE CARRINHO PARA CARREGAR", options)
        if opt == len(options)-1:
            return
        else:
            shcart.load_cart(f"data/shoppingcarts/{options[opt]}.json")

        self.__func_shopping_cart(shcart)

    def __func_shopping_cart(self, shcart):
        options = [
            "Adicionar novos produtos",
            "Adicionar produtos já existentes no carrinho",
            "Remover produtos",
            "Visualizar carrinho",
            "Salvar carrinho",
            "Sair"
        ]

        while True:
            opt = self.__menu_option_selection("MONTAR CARRINHO", options)
            if opt == len(options)-1:
                exit_confirm = self.__menu_option_selection("Alterações não salvas serão perdidas", ["Sair mesmo assim", "Cancelar"])
                if exit_confirm== 0:
                    return

            elif opt == 0:
                produtos = self.__opt_search(return_results= True)
                options_products = [f"{prd.single_price} {prd.name}" for prd in produtos]
                options_products.append("Sair")
                if len(options_products) > 1:
                    prd_select = self.__menu_option_selection("SELECIONE O PRODUTO PARA ADICIONAR", options_products)
                    if prd_select == len(options_products)-1:
                        pass
                    else:
                        produtos[prd_select].print_info()
                        qtd = input("Quantos deseja adicionar ao carrinho? ")
                        if qtd == "":
                            pass
                        else:
                            try:
                                qtd = int(qtd)
                                if qtd > 0:
                                    shcart.add_product(produtos[prd_select], qtd)
                                    plural = "s" if qtd>1 else ""
                                    print(f"Produto{plural} adicionado{plural} com sucesso!")
                            except ValueError:
                                print("Valor inválido")

            elif opt == 1:
                options_products = [f"{prd.get_quantity()}x {prd.get_product().single_price} {prd.get_product().name}" for prd in shcart.items]
                options_products.append("Sair")
                if len(options_products) > 1:
                    prd_select = self.__menu_option_selection("SELECIONE O PRODUTO PARA ADICIONAR", options_products)
                    if prd_select == len(options_products)-1:
                        pass
                    else:
                        shcart.items[prd_select].get_product().print_info()
                        qtd = input("Quantos deseja adicionar do carrinho? ")
                        if qtd == "":
                            pass
                        else:
                            try:
                                qtd = int(qtd)
                                if qtd > 0:
                                    shcart.add_product(shcart.items[prd_select].get_product().name, qtd)
                                    plural = "s" if qtd>1 else ""
                                    print(f"Produto{plural} adicionado{plural} com sucesso!")
                            except ValueError:
                                print("Valor inválido")

            elif opt == 2:
                options_products = [f"{prd.get_quantity()}x {prd.get_product().single_price} {prd.get_product().name}" for prd in shcart.items]
                options_products.append("Sair")
                if len(options_products) > 1:
                    prd_select = self.__menu_option_selection("SELECIONE O PRODUTO PARA REMOVER", options_products)
                    if prd_select == len(options_products)-1:
                        pass
                    else:
                        shcart.items[prd_select].get_product().print_info()
                        qtd = input("Quantos deseja remover do carrinho? ")
                        if qtd == "":
                            pass
                        else:
                            try:
                                qtd = int(qtd)
                                if qtd > 0:
                                    shcart.remove_product(shcart.items[prd_select].get_product().name, qtd)
                                    plural = "s" if qtd>1 else ""
                                    print(f"Produto{plural} removido{plural} com sucesso!")
                            except ValueError:
                                print("Valor inválido")

            elif opt == 3:
                options_visual_keys = [
                    "promo_price",
                    "single_price",
                    "total_parcels_price",
                    "parcel_price"
                ]

                options_visual_pretty = [
                    "Preço promocional/À vista",
                    "Preço à vista",
                    "Preço total parcelado",
                    "Preço das parcelas",
                    "Sair"
                ]

                opt_visual = self.__menu_option_selection("Alterações não salvas serão perdidas", options_visual_pretty)
                if opt_visual == len(options)-1:
                    pass
                else:
                    shcart.print_info(options_visual_keys[opt_visual])

            elif opt == 4:

                _, _, savefiles = next(walk("data/shoppingcarts"))
                exisisting_files = []
                for item in savefiles:
                    exisisting_files.insert(0, str(item)[:-5])

                shcart.print_info('single_price')
                cancel_signal = False
                while True:
                    filename = input("\nInsira o nome desse carrinho: ")

                    try:
                        index_value = exisisting_files.index(filename)
                    except ValueError:
                        index_value = -1

                    if index_value >= 0:
                        print(f"\nCARRINHO {filename}\n")
                        shcart_temp = ShoppingCart()
                        shcart_temp.load_cart(f"data/shoppingcarts/{filename}.json")
                        shcart_temp.print_info('single_price')

                        overwrite_confirm = self.__menu_option_selection("Esse carrinho já existe, deseja sobrescrever?", ["Sim", "Escolher outro nome","Cancelar"])

                        if overwrite_confirm == 0:
                            break
                        
                        elif overwrite_confirm == 1:
                            pass

                        elif overwrite_confirm == 2:
                            cancel_signal = True
                            break

                    if not cancel_signal:
                        shcart.save_cart(f"data/shoppingcarts/{filename}.json")
                        break

    def __func_search(self, category="", must_include=None, dont_include=None):

        def aux_find_must_include(prod):
            if must_include is None or len(must_include) < 1:
                return True

            for element in must_include:
                if (prod.name.lower()).find(element.lower()) == -1:
                    return False

            return True

        def aux_find_dont_include(prod):
            if dont_include is None or len(dont_include) < 1:
                return True

            for element in dont_include:
                if (prod.name.lower()).find(element.lower()) != -1:
                    return False

            return True

        path = "pathtest/teste.html"
        if category == "":
            tag = str(must_include).replace("[","").replace("]","").replace(",","").replace("'","")
            url = url_search(tag)
        else:
            url = url_category(category)

        scr.get_html_file(url, path)
        html_info = scr.read_file(path)

        products = get_products(html_info)

        for i in range(len(products)-1,0,-1):
            if not products[i].available or not aux_find_dont_include(products[i]) or not aux_find_must_include(products[i]):
                products.pop(i)
        
        return products
        

