from locust import events
from locust.runners import MasterRunner, WorkerRunner
from dotenv import load_dotenv
from common.kpi_checker import validate_KPIs
from common.commons import validateTestRunResult
import os

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    load_dotenv(override=True)  # take environment variables from .env.

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Finished the test execution")

@events.quitting.add_listener
def do_checks(environment, **kwargs):
    if isinstance(environment.runner, WorkerRunner):
        return

    stats = environment.runner.stats.total
    validate_KPIs(environment, stats)

    KPIsresult = validateTestRunResult(environment.process_exit_code)