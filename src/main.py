import argparse
import setup_environment
import credentials
import get_collectors
import os
import sys
from datetime import datetime


def main(collector):
    if os.path.exists('private/collectors.txt'):
        os.remove('private/collectors.txt')
    creds = credentials.get_sumo_auth()
    url = f'https://api.sumologic.com/api/v1/collectors'
    if collector == 'all':
        sumo_collector_id = None
        run = 0
        offset_check = True
        try:
            while offset_check:
                if run == 0:
                    offset = 0
                    limit = 33000
                    collector_config = get_collectors.Collectors(offset, limit, sumo_collector_id, url, creds, logger)
                    collector_config.pull_all_collectors()
                    run += 1
                elif run == 1:
                    offset = 33001
                    limit = 66000
                    collector_config = get_collectors.Collectors(offset, limit, sumo_collector_id, url, creds, logger)
                    collector_config.pull_all_collectors()
                    run += 1
                else:
                    offset = 66001
                    limit = 99000
                    collector_config = get_collectors.Collectors(offset, limit, sumo_collector_id, url, creds, logger)
                    collector_config.pull_all_collectors()
                    run += 1
                    offset_check = False
        except Exception as e:
            logger.critical(f'error pulling collectors {e}')
    else:
        offset = None
        limit = None
        collector_config = get_collectors.Collectors(offset, limit, collector, url, creds, logger)
        collector_config.pull_collector()


if __name__ == '__main__':
    start = datetime.now()
    log_date = start.strftime("%Y_%m_%d_%H_%M_%S")
    logger = setup_environment.get_logger(start, './logs/sumologic_api.log')
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--collectorId", nargs="?", default="help", action="store")
        args = parser.parse_args()
        collector_id = args.collectorId
    except Exception as error:
        print(error)
    else:
        if collector_id == 'help':
            selection = input(f'------------------------------------------------------------------\n'
                              f'usage: main.py [-h] [--collectorId=[COLLECTORID]\n\n'
                              f'options:\n'
                              f'-h, --help            show this help message and exit\n'
                              f'    --collectorId=[COLLECTORID]\n'
                              f'    --collectorId=all\n'
                              f'------------------------------------------------------------------\n')
            sys.exit(0)
        else:
            main(collector_id)
