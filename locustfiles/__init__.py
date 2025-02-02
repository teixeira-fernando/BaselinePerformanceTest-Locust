from locust import events
from locust.runners import MasterRunner, WorkerRunner
from dotenv import load_dotenv
from common.kpi_checker import validate_KPIs
from common.commons import validateTestRunResult
import os

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    load_dotenv(override=True)  # take environment variables from .env.
    
@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--my-argument", type=str, env_var="LOCUST_MY_ARGUMENT", default="", help="It's working")
    # Choices will validate command line input and show a dropdown in the web UI
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev", help="Environment")
    # Set `include_in_web_ui` to False if you want to hide from the web UI
    parser.add_argument("--my-ui-invisible-argument", include_in_web_ui=False, default="I am invisible")
    # Set `is_secret` to True if you want the text input to be password masked in the web UI
    parser.add_argument("--my-ui-password-argument", is_secret=True, default="I am a secret")
    # Use a boolean default value if you want the input to be a checkmark
    parser.add_argument("--my-ui-boolean-argument", default=True)
    # Set `is_required` to mark a form field as required
    # parser.add_argument("--my-ui-required-argument", is_required=True, default="I am required")

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