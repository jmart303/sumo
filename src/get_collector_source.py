def pull_sources(name, collector_id, creds, logger):
    import json

    import requests
    url = 'https://api.sumologic.com/api/v1/collectors/'+str(collector_id)+'/sources'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+creds,
        'Cache-Control': 'no-cache'
    }
    response = requests.request('GET', url, headers=headers)
    source_list = json.loads(response.text)
    count = 0
    mylist = [name, collector_id, name]
    try:
        while True:
            source_name = source_list['sources'][count]['name']
            category = source_list['sources'][count]['category']
            log_names = source_list['sources'][count]['logNames']
            mylist.append(count)
            mylist.append(source_name)
            mylist.append(log_names)
            mylist.append(category)
            count += 1
    except Exception as e:
        print('End of source list for', collector_id, 'logging and moving on')
    print(mylist)
    return mylist

