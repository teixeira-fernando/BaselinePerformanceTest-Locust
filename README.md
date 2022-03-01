# Baseline Performance Tests with Locust, Docker-compose and Github-Actions
Locust is a python based load testing framework. Documentation can be found here: [Documentation](https://docs.locust.io/en/stable/index.html)

## Installation
Since we are working with a docker-compose setup, you just need to have docker installed in your machine. 

## Run distributed tests in headless mode - docker-compose
You can run distributed tests with docker-compose and easily scale more workers: [Distributed tests](https://docs.locust.io/en/stable/running-locust-docker.html)
1. Check if the .env file contains the correct configuration for your test run
2. Run `docker-compose up --scale worker=4` with as many workers as you want
3. After your test, run `docker-compose down` or just press `Ctrl + C` if you are running the docker-compose in interactive mode

## Project Structure
* `__init__.py`: Here we have the setup and teardown for our tests. You can insert here anything that needs to be executed at the beginning and at the end of the test execution
* `.env`: This is the general config file. You can specify some parameter values like host, locust file, etc.
* `data/*.py`: We separated the query and filter values into separated test data files, in order to make the tests more readable and maintanable
* `testConfig/*.py`: This folder contains the ramp and KPI configs for each specific performance test
* `common/*.py`: Here we have shared functions and values that are applied in multiple test files
* `kpi_checker.py`: This file contains auxiliary methods necessary for the automated KPI validation
* `*load_test.py`: These are our performance test files. They include our requests and other additional information
* `*load_test_custom_shape.py`: This is the custom ramp configuration, that is imported and used by the different load tests

## RPS checks
We are using a config that enable us to provide a few KPIs goals for a tests excution through environment variables. Right now, we have the possibility to use 5 KPIs:
* RPS
* Maximum fail ratio
* 90% response time percentile
* 95% response time percentile
* 99% response time percentile

The values are passed to locust through command line. Since we are using docker-compose setup, you can check and edit the KPI goals using the .env file.

When the results don't achieve the KPI goals, we have messages returned in the terminal and a different exit code (code 3) of the script, that can be used to integrate with other tools, like for example Jenkins:

```
master_1  | [2021-10-07 21:35:01,009] dc53ec78188f/INFO/root: CHECK FAILED: 90% percentile was 300.0 ms (threshold 200.0 ms)
master_1  | [2021-10-07 21:35:01,009] dc53ec78188f/INFO/root: CHECK SUCCESSFUL: 95% percentile was 360.0 ms (threshold 500.0) ms
master_1  | [2021-10-07 21:35:01,009] dc53ec78188f/INFO/root: CHECK SUCCESSFUL: 99% percentile was 910.0 ms (threshold 1000.0) ms
master_1  | [2021-10-07 21:35:01,010] dc53ec78188f/INFO/root: CHECK FAILED: total rps was 3.6 (threshold 10.0)
master_1  | [2021-10-07 21:35:01,010] dc53ec78188f/INFO/locust.main: Shutting down (exit code 3), bye.
```

If necessary, it is possible to also add more KPIs to be validated. We just need to get it from the metrics that locust provide us: [Locust_stats](https://github.com/locustio/locust/blob/master/locust/stats.py)

The KPIs validation is possible due to a locust plugin. You can get more info about that in this link: [Locust_plugins](https://github.com/SvenskaSpel/locust-plugins/blob/master/locust_plugins/__init__.py)