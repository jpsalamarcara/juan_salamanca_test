import os
import logging

logger = None


def config_env_var(var, value, log=True):
    if var not in os.environ.keys():
        os.environ[var] = value
    if log:
        logger.info('{}: {}'.format(var, os.environ[var]))


def config_env():
    global logger
    config_env_var('LOGS_DIR', '/var/tmp', False)
    basedir = os.path.abspath(os.environ['LOGS_DIR'])
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(basedir, 'cache_monitor.log'))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info('BASEDIR: {}'.format(basedir))
    config_env_var('REDIS_HOST', 'localhost')
    config_env_var('LAT_LONG', '25.759557,-80.374231')
    config_env_var('REGION', 'florida')
    config_env_var('EXPIRE_TIME', '3600')
    config_env_var('ROUTER_HOST', 'localhost:8080')
    config_env_var('DEBUG', '1')


config_env()
