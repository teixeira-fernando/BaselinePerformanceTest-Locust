import logging

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