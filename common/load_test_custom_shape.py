from locust import task, constant, between, LoadTestShape
from commons import readRampConfig
from kpi_checker import validate_metric_goal
import os
from dotenv import load_dotenv


#This shape class will increase user_count in blocks of spawn_rate rampEveryXseconds and then stop the load test after the time_limit
class MyCustomShape(LoadTestShape):
    load_dotenv(override=True)  # take environment variables from .env.
    ramp_config = readRampConfig(os.environ.get("LOCUST_LOCUSTFILE"))
    time_limit_in_seconds = ramp_config.get('time_limit_in_seconds') 
    spawn_rate = ramp_config.get('spawn_rate') 
    ramp_every_X_seconds = ramp_config.get('ramp_every_X_seconds')
    initial_users = ramp_config.get('initial_users')
    max_users = ramp_config.get('max_users')

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_limit_in_seconds:
            user_count = self.initial_users + round(run_time/self.ramp_every_X_seconds)*self.spawn_rate
            if user_count < self.max_users:
                return (user_count, self.spawn_rate)
            else:
                return (self.max_users, self.spawn_rate)

        return None