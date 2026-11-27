from locust import task, constant
from locust.contrib.fasthttp import FastHttpUser
from data.country_info import query_country_info
from common.load_test_custom_shape import MyCustomShape
from common.commons import processResponse, setRampConfig, setKPIConfig
from testConfig.country_info_test_config import COUNTRY_INFO_KPIS, COUNTRY_INFO_RAMP
import __init__


class CountryInfoUser(FastHttpUser):
    wait_time = constant(10)
    basePath = "/"
    setRampConfig(COUNTRY_INFO_RAMP)
    setKPIConfig(COUNTRY_INFO_KPIS)

    def get_country_info(self):
        with self.client.post(
            self.basePath, json={"query": query_country_info},
            catch_response=True, name="Get Country Info"
        ) as response:
            processResponse(response)

    @task
    def requests(self):
        self.get_country_info()