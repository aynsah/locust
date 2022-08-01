from locust import TaskSet, constant, task, between, constant
from utils.config import SharedData, base_url, headers
from utils.err import log

class Account(TaskSet):
    # wait_time = between(0.1, 2)
    wait_time = constant(0.1)

    def on_start(self):
        print("start profile")
        if SharedData.user_id == 0:
            body = SharedData.users[0]

            merge_cart = ""
            if SharedData.cart_token != "":
                merge_cart = "?merge_cart=" + SharedData.cart_token
            
            with self.client.post(base_url() + "/account/do/sign-in" + merge_cart, json=body, headers=headers(), name="login-user") as response:
                try:
                    if response.status_code >= 400:  raise Exception("error status code")

                    SharedData.token = "Bearer " + response.json().get("data").get("access_token")
                    SharedData.user_id = response.json().get("data").get("customer").get("id")
                    SharedData.cart_token = response.json().get("data").get("customer").get("cart").get("cart").get("cart_token")

                except Exception as e:
                    log(response.status_code, response.url, e, response.text)

    @task(1)
    def info(self):
        with self.client.get(base_url() + "/profile/info", headers=headers(), name="user-info") as response:
            try:
                if response.status_code >= 400:  raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(1)
    def loyalty_point(self):
        with self.client.get(base_url() + "/profile/loyalty-points", headers=headers(), name="user-loyalty-point") as response:
            try:
                if response.status_code >= 400:  raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)
         
    @task(1)
    def my_reviews(self):
        with self.client.get(base_url() + "/profile/reviews", headers=headers(), name="user-reviews") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(2)
    def reviewable_items(self):
        with self.client.get(base_url() + "/profile/reviews/reviewable-items", headers=headers(), name="user-reviewable-items") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(2)
    def finish(self):
        print("finish profile")
        self.interrupt()
