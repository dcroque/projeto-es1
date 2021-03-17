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
        for i in range(len(self.items)):
            if self.items[i].get_product().name == product:
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
                    self.items[i].dec_product(quantity)
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
        with open(filepath) as json_file:
            load_data = json.load(json_file)
        for element in load_data['items']:
            prd = Product()
            prd.set_all_by_json(element['product'])
            item = ShoppingCartItem(prd, int(element['quantity']))
            self.add_item(item)

    def save_cart(self, filepath):
        save_data = {'items': []}
        for element in self.items:
            prd = element.get_product()
            qty = element.get_quantity()
            item = {'quantity': int(qty),
                    'product': prd.get_all_in_json()}
            save_data['items'].append(item)
        with open(filepath, 'w+') as json_file:
            json.dump(save_data, json_file, indent= 4, ensure_ascii=False)

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
            self.total_parcels_price += self.__price_to_float(item.get_product().total_parcels_price) * item.get_quantity()

    def __update_parcels_price(self):
        self.parcel_price = self.total_parcels_price/self.n_parcels

    def print_info(self, price_type):
        price_map = {
            "promo_price": "Preço promocional/À vista",
            "single_price": "Preço à vista",
            "total_parcels_price": "Preço total parcelado",
            "parcel_price": "Preço das parcelas"
        }

        if price_type == "parcel_price":
            parcels = f"{self.n_parcels}x"
        else:
            parcels = "1x"
        total_price = str("{:.2f}".format(getattr(self, price_type))).replace('.', ',')

        print("QTD   PREÇO\tPRODUTO")
        for element in self.items:
            el_price = "{:.2f}".format(self.__price_to_float(getattr(element.get_product(),price_type)) * (float(getattr(element.get_product(),'n_parcels')) / self.n_parcels))
            print(f"{element.get_quantity()}x R$ {str(el_price).replace('.', ',')}\t{element.get_product().name}")
        print(f"\n{price_map[price_type]}: \n{parcels} R$ {total_price}")

class ShoppingCartItem:
    def __init__(self, product, quantity):
        self.__product = product
        self.__quantity = quantity

    def get_product(self):
        return self.__product

    def get_quantity(self):
        return int(self.__quantity)

    def inc_product(self, inc):
        self.__quantity += inc

    def dec_product(self, dec):
        self.__quantity -= dec

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

        if not self.in_promo:
            self.promo_price = self.single_price

        self.__update_total_parcels_price()

    def set_all_by_json(self, info):
        self.name = info['name']
        self.promo_price = info['promo_price']
        self.single_price = info['single_price']
        self.total_parcels_price = info['total_parcels_price']
        self.parcel_price = info['parcel_price']
        self.n_parcels = info['n_parcels']
        self.available = bool(info['available'])
        self.in_promo = bool(info['in_promo'])

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

    def get_all_in_json(self):
        info = {}
        info['name'] = self.name
        info['promo_price'] = self.promo_price
        info['single_price'] = self.single_price
        info['total_parcels_price'] = self.total_parcels_price
        info['parcel_price'] = self.parcel_price
        info['n_parcels'] = self.n_parcels
        info['available'] = self.available
        info['in_promo'] = self.in_promo
        return info

    def __update_total_parcels_price(self):
        if self.parcel_price != '' and self.n_parcels != '':
            temp = float(self.parcel_price[3:].replace(',', '.'))
            temp = temp * int(self.n_parcels)
            self.total_parcels_price = "R$ " + ("{:.2f}".format(temp)).replace('.', ',')

    def print_info(self):
        info = self.get_all()
        label = [    "NOME: ", "PRECO PROMOCAO: ", 
                    "PRECO A VISTA: ", "PRECO PARCELADO: ", 
                    "PARCELAS: ", "NUM PARCELAS: ", 
                    "DISP: ", "PROMOCAO: "]
        for i in range(8):
            print(label[i]+str(info[i]))
        print()
