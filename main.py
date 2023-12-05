import json
import gzip
import time
import requests
from httplib2 import Http
from datetime import datetime

def send_notification(message):
    url = 'https://chat.googleapis.com/v1/spaces/AAAAjjBB5BA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=J-YBWtuDPVkgt55lpuLZ1du4_N8gEr8U4sPJQYhQzzY'
    bot_message = {'text': f'Notification {datetime.now()}\n\n{message}'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=json.dumps(bot_message),
    )
    print(response)

with open('last_run_info.txt') as f:
	last_update_time = f.read()
print(last_update_time)

api_key = '9b357357-15c3-4561-a69b-3c4f6aeda953'
url = 'https://services.nvd.nist.gov/rest/json/cvehistory/2.0/?'

# Create a dictionary for headers
headers = {
    'Authorization': f'Bearer {api_key}',  # or 'ApiKey {api_key}' depending on the API requirement
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    response_data = json.loads(response.content)
    current_timestamp = response_data['timestamp']
    new_url = url+f'changeStartDate={last_update_time}%2B01:00&changeEndDate={current_timestamp}%2B01:00'
    response = requests.get(new_url, headers = headers)
    # response = requests.get('https://services.nvd.nist.gov/rest/json/cvehistory/2.0/?changeStartDate=2023-12-02T16:20:26.103%2B01:00&changeEndDate=2023-12-03T16:31:10.490%2B01:00', headers=headers)
    # print(new_url)
    changed_cves = []
    if response.status_code==200:
    	print('Success')
    	response_data = json.loads(response.content)
    	for change in response_data['cveChanges']:
    		changed_cves.append(change['change']['cveId'])

    else:
    	print(f'Error:{response.content}')
print(changed_cves)

update_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={}'
for cve in changed_cves:
	new_url = update_url.format(cve)
	response = requests.get(new_url, headers = headers)
	if response.status_code==200:
		year = cve.split('-')[1]
		print('Success')
		response_data = json.loads(response.content)
		# Reading the JSON data from a gzip file
		with gzip.open(f'cves/{year}', 'rt', encoding='UTF-8') as gzip_file:
		    json_data = gzip_file.read()
		    # Parse the JSON data
		    data = json.loads(json_data)
		data[cve] = response_data['vulnerabilities'][0]['cve']
		with gzip.open(f'cves/{year}', 'wt', encoding='UTF-8') as gzip_file:
		    gzip_file.write(json.dumps(data))

	else:
		print(f'Error:{response.content}')
	time.sleep(6)
with open('last_run_info.txt','w') as f:
	f.write(current_timestamp)
message = f'Updated {len(changed_cves)} CVEs. Here is the list:{changed_cves}'
send_notification(message)

# https://services.nvd.nist.gov/rest/json/cvehistory/2.0/?changeStartDate=2021-08-04T13:00:00.000%2B01:00&changeEndDate=2021-10-22T13:36:00.000%2B01:00
# https://services.nvd.nist.gov/rest/json/cvehistory/2.0/?changeStartDate=2023-12-03T16:20:26.103%2B01:00&changeEndDate=2023-12-03T16:31:10.490%2B01:00
