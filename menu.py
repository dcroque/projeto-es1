from terabyte_scrapper import *
from classes import *
from os import walk

class UserInterface:
	def __init__(self):
		 self.options = [
			 ["Nova compra", self.opt_new_cart],
			 ["Carregar compra", self.opt_load_cart],
			 ["Procurar", self.opt_search],
			 ["Sair", self.opt_exit]
		 ]

	def __menu_option_selection(self, label, options):
		while True:
			print(f"\n===== {label} =====\n")
			for i in range(len(options)):
				print(f"{i+1}: {options[i]}")
			choice = input("\nChoose an option: ")
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


	def opt_exit(self):
		exit()

	def opt_search(self, return_results=False):
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
				if return_results:
					return results
				for item in results:
					item.print_info()
				if not len(results):
					print(f"Parece que nada foi encontrado com as palavras {include_filters} :(")

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
				
	def opt_new_cart(self):
		shcart = ShoppingCart()
		#Carrinho vazio
		self.__func_shopping_cart(shcart)

	def opt_load_cart(self):
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
			"Adicionar produtos",
			"Remover produtos",
			"Visualizar carrinho",
			"Salvar carrinho",
			"Sair"
		]

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
		

