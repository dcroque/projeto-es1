from terabyte_scrapper import *
from classes import *

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
		tag = input()
		self.__func_search(tag, must_include=["processador"], dont_include=["amd"])

	def opt_new_cart(self):
		print(f"Opcao {1} nao implementado ainda")

	def opt_load_cart(self):
		print(f"Opcao {2} nao implementado ainda")

	def __func_search(self, tag, must_include=None, dont_include=None):

		def aux_find_must_include(prod):
			if must_include is None or len(must_include) < 1:
				return True

			all_found = True
			for element in must_include:
				if (prod.name.lower()).find(element.lower()) == -1:
					all_found = False

			return all_found

		def aux_find_dont_include(prod):
			if dont_include is None or len(dont_include) < 1:
				return True

			all_found = True
			for element in dont_include:
				if (prod.name.lower()).find(element.lower()) != -1:
					all_found = False

			return all_found

		path = "pathtest/teste.html"
		url = url_search(tag)

		scr.get_html_file(url, path)
		html_info = scr.read_file(path)

		products = get_products(html_info)

		for item in products:
			if item.available and aux_find_must_include(item) and aux_find_dont_include(item):
				item.print_info()
		

