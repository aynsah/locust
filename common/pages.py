from locust import TaskSet, constant, task, between, constant
from utils.config import SharedData, base_url, headers
from utils.err import log
import random

class Pages(TaskSet):
    # wait_time = between(0.1, 2)
    wait_time = constant(0.1)

    def on_start(self):
        print("start pages")

    @task(1)
    def faq(self):
        with self.client.get(base_url() + "/faq", headers=headers(), name="page-faq") as response:
            try:
                if response.status_code >= 400:  raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(1)
    def about_us(self):
        with self.client.get(base_url() + "/about-us", headers=headers(), name="page-about-us") as response:
            try:
                if response.status_code >= 400:  raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)
         
    @task(1)
    def terms(self):
        with self.client.get(base_url() + "/terms-and-policy", headers=headers(), name="page-terms-and-policy") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(1)
    def testimonials(self):
        with self.client.get(base_url() + "/testimonial/lists", headers=headers(), name="page-testimonials") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(1)
    def articles(self):
        with self.client.get(base_url() + "/article/lists", headers=headers(), name="page-articles") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code")

                articles = response.json().get("data")
                for article in articles:
                    # perbandingan user membuka detail article
                    if random.randint(1, 6) == 1: self.show_article(article["id"])

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    def show_article(self, article_id):
        with self.client.get(base_url() + "/article/show/" + str(article_id), headers=headers(), name="page-article-show") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code")

            except Exception as e:
                log(response.status_code, response.url, e, response.text)

    @task(2)
    def finish(self):
        print("finish pages")
        self.interrupt()
