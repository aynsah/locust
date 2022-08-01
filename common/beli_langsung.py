from email import header
import random
import string

from locust import TaskSet, task, between, constant
from common.location import Location

from utils.config import SharedData, base_url, headers
from utils.err import log

class BeliLangsung(TaskSet):
    # wait_time = between(1, 3)
    wait_time = constant(0.1)

    code = ""
    items = []

    catalog_page = 1
    
    def on_start(self):
        print("start beli langsung")
        while len(self.items) == 0:
            self.list_catalog()

    @task
    def set_promo_code(self):
        with self.client.get(base_url() + "/profile/promotion-codes/?data_testing=true&per_page=-1&search_column=code&search_text=&search_condition=!=", headers=headers(), name="promo-code-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                vouchers = response.json().get("data")
                total = response.json().get("meta").get("total") - 1

                selected_voucher = random.randint(-1, total)
                promo_code = "" if selected_voucher == -1 else str(vouchers[selected_voucher]["code"])

                self.code = promo_code
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task
    def checkout(self):
        checkout_body = {
            "items": self.items,
            "payment_mode_id": 1,
            "shipping_service": "OKE",
            "shipping_id": "JNE",
            "shipping_amount": 22000,
            "discount_voucher_code": self.code
        }            

        if SharedData.user_id != 0:
            checkout_body["shipping_customer_address_id"] = Location.choose_address(self)
        else:
            state_id, city_id = Location.choose_state(self)
            profile = {
                "phone": self.generate_random_phone(),
                "state_id": state_id,
                "city_id": city_id
            }
            checkout_body["profile"] = profile        

        with self.client.post(base_url() + "/orders/checkout/test", json=checkout_body, headers=headers(), name="checkout-beli-langsung") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

        print("finish beli langsung")
        self.interrupt()

    def list_catalog(self):
        with self.client.get(base_url() + "/catalog/lists?page=" + str(self.catalog_page), headers=headers(), name="catalog-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                total_page = response.json().get("meta").get("total_page")
                go_next = random.randint(0, 1)
                self.catalog_page = self.catalog_page + 1 if go_next else random.randint(1, total_page)
                    
                products = response.json().get("data")
                for product in products:
                    is_out_of_stock = product["is_out_stock"]
                    # perbandingan user membuka detail product
                    if random.randint(1, 6) == 1 and not is_out_of_stock: self.show_catalog(product["id"])

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    def show_catalog(self, id):
        with self.client.get(base_url() + "/catalog/show/" + str(id), headers=headers(), name="catalog-show") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 
                
                product = response.json().get("data")
                stock = product["total_qty"]

                # perbandingan user ingin memasukan kedalam cart
                if random.randint(1, 8) == 1 and stock > 0:
                    # -1 == tanpa variant
                    variants = product.get("variant")
                    random_variant = random.randint(-1, len(variants) - 1)
                    variant_id = 0 if random_variant == -1 else variants[random_variant]["id"]

                    if variant_id != 0:
                        stock = variants[random_variant]["total_qty"]
                    if stock > 0: 
                        max_quantity = min(5, stock)

                        self.generate_cart(product["id"], variant_id, "product", random.randint(1, max_quantity), self.random_notes(), [])
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    def generate_cart(self, item_id, item_variant_id, item_type, quantity, notes, subitems):
        body = {
            "items": [
                {
                    "item_id": item_id,
                    "item_variant_id": item_variant_id,
                    "type": item_type,
                    "quantity": quantity,
                    "notes": notes,
                    "subitems": subitems,
                }
            ]
        }

        with self.client.post(base_url() + "/cart/generate", json=body, headers=headers(), name="generate-cart") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                items = response.json().get("data").get("cart").get("items")
                if items == None: self.interrupt()
                if len(items) == 0: self.interrupt()

                self.items = items
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @staticmethod
    def random_notes():
        notes = ""
        for _ in range(random.randint(4, 20)):
            notes += random.choice(string.ascii_letters)

        return notes

    @staticmethod
    def generate_random_phone():
        return "+62" + str(random.randint(80000000000, 89999999999))