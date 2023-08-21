from locust import task, constant
from locust.contrib.fasthttp import FastHttpUser
from data.previous_launches_info import query_previous_launches_info
from common.load_test_custom_shape import MyCustomShape
from common.commons import processResponse, setRampConfig, setKPIConfig
from testConfig.previous_launches_test_config import PREVIOUS_LAUNCHES_INFO_KPIS, PREVIOUS_LAUNCHES_INFO_RAMP
import os
import gevent
import __init__

class PreviousLaunchesInfoUser(FastHttpUser):
    wait_time = constant(10)
    basePath = "/"
    setRampConfig(PREVIOUS_LAUNCHES_INFO_RAMP)
    setKPIConfig(PREVIOUS_LAUNCHES_INFO_KPIS)
    def on_start(self):
        return super().on_start()        
    
    def get_previous_launches_info(self):
      with self.client.post(self.basePath, json={'query': query_previous_launches_info} ,catch_response=True, name="Get Previous Launches Info") as response:
        processResponse(response)
    
    @task
    def requests(self):
      gevent.spawn(self.get_previous_launches_info()) 