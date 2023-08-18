import logging
import os

def validate_metric_goal(environment, metric, metric_goal, description):
    if metric_goal < 0:
        return
    if metric > metric_goal:
        logging.info(
                f"CHECK FAILED: {description} was {metric:.1f} (threshold {metric_goal:.1f})"
            )
        environment.process_exit_code = 3
    else:
        logging.info(
                f"CHECK SUCCESSFUL: {description} was {metric:.1f} (threshold {metric_goal:.1f})"
            )

def validate_rps(environment, metric, metric_goal, description):
    if metric_goal < 0:
        return
    if metric < metric_goal:
        logging.info(
                f"CHECK FAILED: {description} was {metric:.1f} (threshold {metric_goal:.1f})"
            )
        environment.process_exit_code = 3
    else:
        logging.info(
                f"CHECK SUCCESSFUL: {description} was {metric:.1f} (threshold {metric_goal:.1f})"
            )
        
def validate_KPIs(environment, stats):
    percentile_90 = stats.get_response_time_percentile(0.90)
    percentile_95 = stats.get_response_time_percentile(0.95)
    percentile_99 = stats.get_response_time_percentile(0.99)
    RPS = stats.total_rps
    fail_ratio = stats.fail_ratio

    check_rps = float(os.environ.get('REQUESTS_PER_SECOND'))
    check_fail_ratio = float(os.environ.get('FAIL_RATIO_ALLOWED'))
    check_response_time_90_percentile = int(os.environ.get('RESPONSE_TIME_PERCENTILE_90_MILLISECONDS'))
    check_response_time_95_percentile = int(os.environ.get('RESPONSE_TIME_PERCENTILE_95_MILLISECONDS'))
    check_response_time_99_percentile = int(os.environ.get('RESPONSE_TIME_PERCENTILE_99_MILLISECONDS'))

    validate_metric_goal(environment, percentile_90, check_response_time_90_percentile, "90% percentile (ms)")
    validate_metric_goal(environment, percentile_95, check_response_time_95_percentile, "95% percentile (ms)")
    validate_metric_goal(environment, percentile_99, check_response_time_99_percentile, "99% percentile (ms)")
    validate_rps(environment, RPS, check_rps, "Requests per second")
    validate_metric_goal(environment, fail_ratio, check_fail_ratio, "Fail ratio")