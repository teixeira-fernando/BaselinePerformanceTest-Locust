from locust import events
from locust.runners import MasterRunner, WorkerRunner
from dotenv import load_dotenv
from kpi_checker import validate_metric_goal, validate_rps
from common.commons import validateTestRunResult, readRampConfig, readKPIsConfig
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
    percentile_90 = stats.get_response_time_percentile(0.90)
    percentile_95 = stats.get_response_time_percentile(0.95)
    percentile_99 = stats.get_response_time_percentile(0.99)
    RPS = stats.total_rps
    fail_ratio = stats.fail_ratio

    kpis_config = readKPIsConfig(os.environ.get("LOCUST_LOCUSTFILE"))
    check_rps = kpis_config.get('requests_per_second') 
    check_fail_ratio = kpis_config.get('fail_ratio_allowed') 
    check_response_time_90_percentile = kpis_config.get('response_time_percentile_90_milliseconds')
    check_response_time_95_percentile = kpis_config.get('response_time_percentile_95_milliseconds')
    check_response_time_99_percentile = kpis_config.get('response_time_percentile_99_milliseconds')

    validate_metric_goal(environment, percentile_90, check_response_time_90_percentile, "90% percentile (ms)")
    validate_metric_goal(environment, percentile_95, check_response_time_95_percentile, "95% percentile (ms)")
    validate_metric_goal(environment, percentile_99, check_response_time_99_percentile, "99% percentile (ms)")
    validate_rps(environment, RPS, check_rps, "Requests per second")
    validate_metric_goal(environment, fail_ratio, check_fail_ratio, "Fail ratio")

    KPIsresult = validateTestRunResult(environment.process_exit_code)