import json
import gzip

with open('sample.json', 'r') as f:
	data = json.load(f)

for year, cve in data.items():
	# Writing the JSON data to a gzip file
	with gzip.open(f'cves/{year}', 'wt', encoding='UTF-8') as gzip_file:
	    gzip_file.write(json.dumps(cve))
	print('Created file for:',year)
	# The file is now saved as 'sample_data.json.gz' in the current directory
