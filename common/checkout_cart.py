import random

from locust import TaskSet, task, between, constant
from common.location import Location

from utils.config import SharedData, base_url
from utils.err import log

class CheckoutCart(TaskSet):
    # wait_time = between(1, 3)
    wait_time = constant(0.1)

    items = []
    code = ""

    def on_start(self):
        print("start checkout")
        if SharedData.cart_token == "": self.interrupt()

        headers = {"Authorization": SharedData.token}

        with self.client.get(base_url() + "/cart/list/" + SharedData.cart_token, headers=headers, name="list-cart") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                items = response.json().get("data").get("cart").get("items")
                if items == None: self.interrupt()
                if len(items) == 0: self.interrupt()

                self.items = items
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)
                self.interrupt()

    @task
    def set_promo_code(self):
        self.code = self.get_promo_code()
        body = {"promo_code": self.code}
        headers = {"Authorization": SharedData.token}

        with self.client.put(base_url() + "/cart/update/" + SharedData.cart_token, json=body, headers=headers, name="promo-code-update") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task
    def checkout(self):
        headers = {"Authorization": SharedData.token}
        body = {
            "items": self.items,
            "payment_mode_id": 1,
            "shipping_service": "OKE",
            "shipping_id": "JNE",
            "shipping_amount": 22000,
            "discount_voucher_code": self.code
        }

        if SharedData.user_id != 0:
            body["shipping_customer_address_id"] = Location.choose_address(self)
        else:
            state_id, city_id = Location.choose_state(self)
            profile = {
                "phone": self.generate_random_phone(),
                "state_id": state_id,
                "city_id": city_id
            }
            body["profile"] = profile

        with self.client.post(base_url() + "/orders/checkout/test", json=body, headers=headers, name="checkout") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                SharedData.cart_token = ""
                if SharedData.user_id != 0:
                    self.reset_cart()

                print("success checkout")
                    
            except Exception as e:
                print(body)
                log(response.status_code, response.url, e, response.text)

        print("finish checkout")
        self.interrupt()

    def get_promo_code(self):
        promo_code = ""
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/profile/promotion-codes/?data_testing=true&per_page=-1&search_column=code&search_text=&search_condition=!=", headers=headers, name="promo-code-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                vouchers = response.json().get("data")
                total = response.json().get("meta").get("total") - 1

                selected_voucher = random.randint(-1, total)
                promo_code = "" if selected_voucher == -1 else str(vouchers[selected_voucher]["code"])
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

        return promo_code

    def reset_cart(self):
        headers = {"Authorization": SharedData.token}
        body = { "items": [] }

        with self.client.post(base_url() + "/cart/create", json=body, headers=headers, name="reset-cart") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                SharedData.cart_token = response.json().get("data").get("cart").get("cart_token")
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @staticmethod
    def generate_random_phone():
        return "+62" + str(random.randint(80000000000, 89999999999))
