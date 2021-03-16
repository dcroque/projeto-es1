class ShoppingCart:
	def __init__(self):
		self.products = []
		self.promo_price = ''
		self.single_price = ''
		self.total_parcels_price = ''
		self.parcel_price = ''
		self.n_parcels = ''
		self.in_promo = False

	def add_product(self, item, quantity):
		product_name = item.name
		for i in range(len(self.products)):
			if products[i].get_product().name == product_name:
				products[i].add_product(quantity)
				self.__update_prices()
				return
		self.products.append(ShoppingCartItem(item, quantity))
		self.__update_prices()
		
	def remove_product(self, product_name, quantity):
		for i in range(len(self.products)):
			if self.products[i].get_product().name == product_name:
				if quantity >= self.products[i].get_quantity():
					self.products.pop(i)
				else:
					self.products[i].remove_product(quantity)
		self.__update_prices()

	def __update_prices(self):
		if len(self.products) > 0:
			self.__update_promo_price()
			self.__update_single_price()
			self.__update_n_parcels()
			self.__update_total_parcels_price()
			self.__update_parcels_price()
	
	def __update_promo_price(self):
		self.promo_price = 0
		for item in self.products:
			if item.product.in_promo:
				self.promo_price += item.product.promo_price * item.quantity
				self.in_promo = True
			else:
				self.promo_price += item.product.single_price * item.quantity

	def __update_single_price(self):
		self.single_price = 0
		for item in self.products:
			self.single_price += item.product.single_price * item.quantity
	
	def __update_n_parcels(self):
		self.n_parcels = self.products[0].n_parcels
		for item in self.products:
			if item.product.n_parcels < self.n_parcels:
				self.n_parcels = item.product.n_parcels

	def __update_total_parcels_price(self):
		self.total_parcels_price = 0
		for item in self.products:
			self.total_parcels_price += item.product.total_parcels_price * item.quantity

	def __update_parcels_price(self):
		self.parcels_price = self.total_parcels_price/self.n_parcels
	
class ShoppingCartItem:
	def __init__(self, product, quantity):
		self.__product = product
		self.__quantity = quantity

	def get_product(self):
		return self.__product

	def get_quantity(self):
		return self.__quantity

	def add_product(self, inc):
		self.quantity += inc

	def remove_product(self, dec):
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
		label = [	"NOME: ", "PRECO PROMOCAO: ", 
					"PRECO A VISTA: ", "PRECO PARCELADO: ", 
					"PARCELAS: ", "NUM PARCELAS: ", 
					"DISP: ", "PROMOCAO: "]
		for i in range(8):
			print(label[i]+str(info[i]))
		print()
