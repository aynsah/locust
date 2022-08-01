import random

from locust import TaskSet, task, between

from utils.config import SharedData, base_url
from utils.err import log

class Location(TaskSet):

    def choose_address(self):
        if SharedData.user_id == 0: return 0

        address_id = 0
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/profile/addresses/list?per_page=-1", headers=headers, name="location-address-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                states = response.json().get("data")
                total = response.json().get("meta").get("total") - 1

                selected_address = random.randint(0, total)
                address_id = states[selected_address]["id"]
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

        return address_id

    def choose_state(self):
        state_id = 0
        city_id = 0
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/country/states?per_page=-1&country_id=ID", headers=headers, name="location-state-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                states = response.json().get("data")
                total = response.json().get("meta").get("total") - 1

                selected_state = random.randint(0, total)
                state_id = states[selected_state]["id"]
                city_id = Location.choose_city(self, state_id)
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

        return state_id, city_id

    def choose_city(self, state_id):
        city_id = 0
        headers = {"Authorization": SharedData.token}
        with self.client.get(base_url() + "/country/state/cities?per_page=-1&state_id=?" + str(state_id), headers=headers, name="location-city-list") as response:
            try:
                if response.status_code >= 400: raise Exception("error status code") 

                cities = response.json().get("data")
                total = response.json().get("meta").get("total") - 1

                selected_city = random.randint(0, total)
                city_id = cities[selected_city]["id"]
                    
            except Exception as e:
                log(response.status_code, response.url, e, response.text)

        return city_id