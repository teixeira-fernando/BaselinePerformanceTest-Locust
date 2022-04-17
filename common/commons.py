from distutils.command.config import config
import json
from testConfig.default_test_config import DEFAULT_RAMP, DEFAULT_KPIS
from testConfig.dragon_info_test_config import DRAGON_INFO_RAMP, DRAGON_INFO_KPIS
from testConfig.previous_launches_test_config import PREVIOUS_LAUNCHES_INFO_RAMP, PREVIOUS_LAUNCHES_INFO_KPIS


ERROR_CODE = 3

def processResponse(response):   
    if (response.status_code == 200 and "errors" in response.json()): #since it is graphql, the responses can occur with a 200 code
        response.failure("We received a response with code "+str(response.status_code)+" and the errors: "+json.dumps(response.json()))    
    elif (response.status_code == 200):
        response.success()

def validateTestRunResult(exit_code):
    if(exit_code == ERROR_CODE):
        return "Failure"
    else:
       return "Success"

def readRampConfig(ramp_config):
    if('dragon' in str(ramp_config).lower()):
        return DRAGON_INFO_RAMP
    if('previous_launches' in str(ramp_config).lower()):
        return PREVIOUS_LAUNCHES_INFO_RAMP
    else:
        return DEFAULT_RAMP

def readKPIsConfig(ramp_config):
    if('dragon' in str(ramp_config).lower()):
        return DRAGON_INFO_KPIS
    if('previous_launches' in str(ramp_config).lower()):
        return PREVIOUS_LAUNCHES_INFO_KPIS
    else:
        return DEFAULT_KPIS
        