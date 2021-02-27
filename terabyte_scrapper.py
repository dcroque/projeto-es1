import scrapper as scr

class Product:
	def __init__(self):
		self.name = ''
		self.promo_price = ''
		self.single_price = ''
		self.total_parcels_price = ''
		self.parcel_price = ''
		self.n_parcels = ''
		self.available = False
		self.in_promo = False

	def set_all(self, info):
		if len(info) != 8:
			return

		self.name = info[0]
		self.promo_price = info[1]
		self.single_price = info[2]
		self.total_parcels_price = info[3]
		self.parcel_price = info[4]
		self.n_parcels = info[5]
		self.available = info[6]
		self.in_promo = info[7]

		self.__update_total_parcels_price()
	
	def get_all(self):
		info = [None]*8
		info[0] = self.name
		info[1] = self.promo_price
		info[2] = self.single_price
		info[3] = self.total_parcels_price
		info[4] = self.parcel_price
		info[5] = self.n_parcels
		info[6] = self.available
		info[7] = self.in_promo
		return info

	def __update_total_parcels_price(self):
		if self.parcel_price != '' and self.n_parcels != '':
			temp = float(self.parcel_price[3:].replace(',', '.'))
			temp = temp * int(self.n_parcels)
			self.total_parcels_price = "R$ " + ("{:.2f}".format(temp)).replace('.', ',')

	def print_info(self):
		info = self.get_all()
		label = [	"NAME: ", "PRECO PROMOCAO: ", 
					"PRECO A VISTA: ", "PRECO PARCELADO: ", 
					"PARCELAS: ", "NUM PARCELAS: ", 
					"DISP: ", "PROMOCAO: "]
		for i in range(8):
			print(label[i]+str(info[i]))
		print()

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
	for cat in category:
		url += "/"+cat
		layer += 1
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

tag = input("O que deseja procurar?")
print()

path = "pathtest/teste.html"
url = url_search(tag)

scr.get_html_file(url, path)
html_info = scr.read_file(path)

produtos = get_products(html_info)

for item in produtos:
	if item.available and (item.name).find(tag) != -1:
		item.print_info()
