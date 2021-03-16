import json

class ShoppingCart:
	def __init__(self):
		self.items = []
		self.promo_price = ''
		self.single_price = ''
		self.total_parcels_price = ''
		self.parcel_price = ''
		self.n_parcels = ''
		self.in_promo = False				

	def add_product(self, product, quantity):
		product_name = product.name
		for i in range(len(self.items)):
			if self.items[i].get_product().name == product_name:
				self.items[i].inc_product(quantity)
				self.__update_prices()
				return
		self.items.append(ShoppingCartItem(product, quantity))
		self.__update_prices()

	def add_item(self,item):
		product_name = item.get_product().name
		for i in range(len(self.items)):
			if self.items[i].get_product().name == product_name:
				self.items[i].inc_product(item.get_quantity())
				self.__update_prices()
				return
		self.items.append(item)
		self.__update_prices()

		
	def remove_product(self, product_name, quantity):
		for i in range(len(self.items)):
			if self.items[i].get_product().name == product_name:
				if quantity >= self.items[i].get_quantity():
					self.items.pop(i)
				else:
					self.items[i].remove_product(quantity)
		self.__update_prices()

	def __reset(self):
		self.items = []
		self.promo_price = ''
		self.single_price = ''
		self.total_parcels_price = ''
		self.parcel_price = ''
		self.n_parcels = ''
		self.in_promo = False

	def load_cart(self, filepath):
		self.__reset()
		
		f = open(filepath)
		data = json.load(f)

        	#for each item add item
 		for i in in data[items]:
			add(i)

	def save_cart(self, filepath):
		#save json
		pass
		

	def __price_to_float(self, strprice):
		return float(strprice[3:].replace(',', '.'))

	def __update_prices(self):
		if len(self.items) > 0:
			self.__update_promo_price()
			self.__update_single_price()
			self.__update_n_parcels()
			self.__update_total_parcels_price()
			self.__update_parcels_price()
	
	def __update_promo_price(self):
		self.promo_price = 0
		for item in self.items:
			if item.get_product().in_promo:
				self.promo_price += self.__price_to_float(item.get_product().promo_price) * item.get_quantity()
				self.in_promo = True
			else:
				self.promo_price += self.__price_to_float(item.get_product().single_price) * item.get_quantity()

	def __update_single_price(self):
		self.single_price = 0
		for item in self.items:
			self.single_price += self.__price_to_float(item.get_product().single_price) * item.get_quantity()
	
	def __update_n_parcels(self):
		self.n_parcels = int(self.items[0].get_product().n_parcels)
		for item in self.items:
			if int(item.get_product().n_parcels) < self.n_parcels:
				self.n_parcels = int(item.get_product().n_parcels)

	def __update_total_parcels_price(self):
		self.total_parcels_price = 0
		for item in self.items:
			self.total_parcels_price += self.__price_to_float(item.get_product().total_parcels_price[3:]) * item.get_quantity()

	def __update_parcels_price(self):
		self.parcels_price = self.total_parcels_price/self.n_parcels
	
class ShoppingCartItem:
	def __init__(self, product, quantity):
		self.__product = product
		self.__quantity = quantity

	def get_product(self):
		return self.__product

	def get_quantity(self):
		return int(self.__quantity)

	def inc_product(self, inc):
		self.quantity += inc

	def dec_product(self, dec):
		self.quantity -= dec

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
		self.promo_price = info[1].replace(".","")
		self.single_price = info[2].replace(".","")
		self.total_parcels_price = info[3]
		self.parcel_price = info[4].replace(".","")
		self.n_parcels = info[5]
		self.available = info[6]
		self.in_promo = info[7]

		if self.in_promo:
			temp = self.single_price
			self.single_price = self.promo_price
			self.promo_price = temp

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
		label = [	"NOME: ", "PRECO PROMOCAO: ", 
					"PRECO A VISTA: ", "PRECO PARCELADO: ", 
					"PARCELAS: ", "NUM PARCELAS: ", 
					"DISP: ", "PROMOCAO: "]
		for i in range(8):
			print(label[i]+str(info[i]))
		print()
