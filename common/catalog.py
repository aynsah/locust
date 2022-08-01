from email import header
import random
import string

from locust import TaskSet, task, between, constant

from utils.config import SharedData, base_url
from utils.err import log

class AccessCatalog(TaskSet):
    # wait_time = between(1, 3)
    wait_time = constant(0.1)

    catalog_page = 1
    catalog_combo_page = 1
    
    def on_start(self):
        print("start catalog")

    @task(3)
    def access_catalog(self):
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/catalog/lists?page=" + str(self.catalog_page), headers=headers, name="catalog-list") as response:
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

    @task(2)
    def access_catalog_combo(self):
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/catalog/combo/lists?page=" + str(self.catalog_combo_page), headers=headers, name="catalog-combo-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                total_page = response.json().get("meta").get("total_page")
                go_next = random.randint(0, 1)
                self.catalog_combo_page = self.catalog_combo_page + 1 if go_next else random.randint(1, total_page)

                combos = response.json().get("data")
                for combo in combos:
                    # perbandingan user membuka detail combo
                    if random.randint(1, 6) == 1: self.show_catalog_combo(combo["id"])

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(1)
    def finish(self):
        print("finish catalog")
        self.interrupt()


    def show_catalog(self, id):
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/catalog/show/" + str(id), headers=headers, name="catalog-show") as response:
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
                    
                    self.add_cart(product["id"], variant_id, "product", random.randint(1, stock), self.random_notes(), [])
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    def show_catalog_combo(self, id):
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/catalog/combo/show/" + str(id), headers=headers, name="catalog-combo-show") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    def add_cart(self, item_id, item_variant_id, item_type, quantity, notes, subitems):
        headers = {"Authorization": SharedData.token}
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

        if SharedData.cart_token != "":
            body["cart_token"] = SharedData.cart_token

        with self.client.post(base_url() + "/cart/create", json=body, headers=headers, name="add-cart") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                SharedData.cart_token = response.json().get("data").get("cart").get("cart_token")
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @staticmethod
    def random_notes():
        notes = ""
        for _ in range(random.randint(4, 20)):
            notes += random.choice(string.ascii_letters)

        return notes