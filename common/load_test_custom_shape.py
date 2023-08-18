from locust import task, constant, between, LoadTestShape
import os
from dotenv import load_dotenv


#This shape class will increase user_count in blocks of spawn_rate rampEveryXseconds and then stop the load test after the time_limit
class MyCustomShape(LoadTestShape):

    def __init__(self):
        self.time_limit_in_seconds = int(os.environ.get("TIME_LIMIT_IN_SECONDS"))
        self.spawn_rate = int(os.environ.get("SPAWN_RATE"))
        self.ramp_every_X_seconds = int(os.environ.get("RAMP_EVERY_X_SECONDS"))  
        self.initial_users = int(os.environ.get("INITIAL_USERS"))
        self.max_users = int(os.environ.get("MAX_USERS"))

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_limit_in_seconds:
            user_count = self.initial_users + round(run_time/self.ramp_every_X_seconds)*self.spawn_rate
            if user_count < self.max_users:
                return (user_count, self.spawn_rate)
            else:
                return (self.max_users, self.spawn_rate)

        return None