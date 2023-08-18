from distutils.command.config import config
import json
import logging
import os

ERROR_CODE = 3

def processResponse(response):   
    if (response.status_code == 200 and "errors" in response.json()): #since it is graphql, the responses can occur with a 200 code
        response.failure("We received a response with code "+str(response.status_code)+" and the errors: "+json.dumps(response.json()))    
    elif (response.status_code == 200):
        logging.info('Response: '+json.dumps(response.json()))
        response.success()

def validateTestRunResult(exit_code):
    if(exit_code == ERROR_CODE):
        return "Failure"
    else:
       return "Success"

def setRampConfig(ramp_config):
    os.environ["TIME_LIMIT_IN_SECONDS"] = str(ramp_config.get('TIME_LIMIT_IN_SECONDS')) 
    os.environ["SPAWN_RATE"] = str(ramp_config.get('SPAWN_RATE'))
    os.environ["RAMP_EVERY_X_SECONDS"] = str(ramp_config.get('RAMP_EVERY_X_SECONDS'))
    os.environ["INITIAL_USERS"] = str(ramp_config.get('INITIAL_USERS')) 
    os.environ["MAX_USERS"] = str(ramp_config.get('MAX_USERS')) 

def setKPIConfig(kpi_config):
    os.environ["REQUESTS_PER_SECOND"] = str(kpi_config.get('REQUESTS_PER_SECOND')) 
    os.environ["FAIL_RATIO_ALLOWED"] = str(kpi_config.get('FAIL_RATIO_ALLOWED'))
    os.environ["RESPONSE_TIME_PERCENTILE_90_MILLISECONDS"] = str(kpi_config.get('RESPONSE_TIME_PERCENTILE_90_MILLISECONDS'))
    os.environ["RESPONSE_TIME_PERCENTILE_95_MILLISECONDS"] = str(kpi_config.get('RESPONSE_TIME_PERCENTILE_95_MILLISECONDS')) 
    os.environ["RESPONSE_TIME_PERCENTILE_99_MILLISECONDS"] = str(kpi_config.get('RESPONSE_TIME_PERCENTILE_99_MILLISECONDS')) 
        