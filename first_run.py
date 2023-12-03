import requests
import json
import time
final_json = {}

api_key = '9b357357-15c3-4561-a69b-3c4f6aeda953'
url = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?'

# Create a dictionary for headers
headers = {
    'Authorization': f'Bearer {api_key}',  # or 'ApiKey {api_key}' depending on the API requirement
}

# Make the base request with the headers
response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_data = json.loads(response.content)
    timestamp = response_data['timestamp']
    total_results = response_data['totalResults']
    resultsperpage = 2000
    startindex = 0
    print('total results:',total_results)
    total_requests = (int(total_results)//2000)+1
    print('total requests:',total_requests)
    temp_json = {}
    with open('last_run_info.txt','w') as f:
        f.write(timestamp)
    for i in range(total_requests):
    	url = '{}resultsPerPage={}&startIndex={}'.format(url,resultsperpage,startindex)
    	print(i, url)
    	response = requests.get(url, headers=headers)
    	if response.status_code == 200:
    		print('success')
    		response_data = json.loads(response.content)
    		for cve in response_data['vulnerabilities']:
    			cve_id = cve['cve']['id']
    			# print(cve_id)
    			temp_json[cve_id] = cve['cve']
    	else:
    		print(f"Error in base request: {response.status_code}. Retrying in 5 sec .........")
    		time.sleep(5)
    		print(i, url)
    		response = requests.get(url, headers=headers)
    		if response.status_code == 200:
    			print('success')
    			response_data = json.loads(response.content)
    			for cve in response_data['vulnerabilities']:
    				cve_id = cve['cve']['id']
    				# print(cve_id)
    				temp_json[cve_id] = cve['cve']

    	for k, v in temp_json.items():
    		year = k.split('-')[1]
    		try:
    			final_json[year].update({k:v})
    		except KeyError:
    			final_json[year] = {k:v}

    	startindex+=2000
    	url = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?'
    	print('Json Ready')
    	time.sleep(6)
    # Process the response here
else:
    print(f"Error in base request: {response.status_code}")
    print(response.text)


for year, cve in final_json.items():
    # Writing the JSON data to a gzip file
    with gzip.open(f'cves/{year}', 'wt', encoding='UTF-8') as gzip_file:
        gzip_file.write(json.dumps(cve))
        
    print('Created file for:',year)
with open("sample.json", "w") as outfile:
    json.dump(final_json, outfile)