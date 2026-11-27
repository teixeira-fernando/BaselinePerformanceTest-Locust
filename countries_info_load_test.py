from locust import task, constant
from locust.contrib.fasthttp import FastHttpUser
from data.countries_info import query_countries_info
from common.load_test_custom_shape import MyCustomShape
from common.commons import processResponse, setRampConfig, setKPIConfig
from testConfig.countries_info_test_config import COUNTRIES_INFO_KPIS, COUNTRIES_INFO_RAMP
import __init__


class CountriesInfoUser(FastHttpUser):
    wait_time = constant(10)
    basePath = "/"
    setRampConfig(COUNTRIES_INFO_RAMP)
    setKPIConfig(COUNTRIES_INFO_KPIS)

    def get_countries_info(self):
        with self.client.post(
            self.basePath, json={"query": query_countries_info},
            catch_response=True, name="Get Countries Info"
        ) as response:
            processResponse(response)

    @task
    def requests(self):
        self.get_countries_info()