import requests
import get_collector_source
import credentials


class Collectors:
    def __init__(self, offset, limit, sumo_collector_id, url, creds, logger):
        self.offset = offset,
        self.limit = limit,
        self.sumo_collector_id = sumo_collector_id,
        self.url = url
        self.creds = creds,
        self.logger = logger

    def pull_all_collectors(self):
        creds = credentials.get_sumo_auth()
        with (open('private/collectors.txt', 'a+') as file):
            try:
                sumo_url = f'{self.url}?offset={self.offset}&limit={self.limit}' \
                    .replace('(', '').replace(')', '') \
                    .replace(',', '').replace("'", '')
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + creds,
                    'Cache-Control': 'no-cache'
                }
                response = requests.request('GET', sumo_url, headers=headers)
                status = response.status_code
                if status == 200:
                    json_data = response.json()
                    for collector in json_data['collectors']:
                        name = collector['name']
                        collector_id = collector['id']
                        file.write(f'{collector_id} {name} \n')
                else:
                    self.logger.critical(f'error connecting to api status code {status}')
            except Exception as e:
                self.logger.critical(f'error getting all collectors, accessing api {e}')

    def pull_collector(self):
        creds = credentials.get_sumo_auth()
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + creds,
                'Cache-Control': 'no-cache'
            }
            collector_id = (f'{self.sumo_collector_id}'.replace('(', '').replace(')', '')
                            .replace(',', '').replace("'", ''))
            sumo_url = f'{self.url}/{collector_id}'
            response = requests.request('GET', sumo_url, headers=headers)
            json_data = response.json()
            c_name = json_data['collector']['name']
            c_id = json_data['collector']['id']
            get_collector_source.pull_sources(c_name, c_id, creds, self.logger)
        except Exception as e:
            self.logger.critical(f'error getting single collector, accessing sumo api {e}')
