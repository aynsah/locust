from locust import HttpUser, task, between
from datetime import datetime

from utils.config import SharedData, base_url
from utils.err import log
from common.catalog import AccessCatalog
from common.account import Account
from common.checkout_cart import CheckoutCart

class HelloWorldUser(HttpUser):
    wait_time = between(0.1, 2)
    tasks = {AccessCatalog:2, CheckoutCart:1}

    def __init__(self, parent):
        super(HelloWorldUser, self).__init__(parent)
        self.now = datetime.now()
        SharedData.now = self.now.strftime("%d%m%Y%H%M%S")

    def on_start(self):
        body = SharedData.client
        with self.client.post(base_url() + "/client/login", json=body, name="login-client") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                SharedData.token = "Bearer " + response.json().get("access_token")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/store/data", headers=headers, name="get-store-data") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                SharedData.lang = response.json().get("data").get("lang_code")
                SharedData.domain = response.json().get("data").get("url_id")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)