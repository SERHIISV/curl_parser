import json

from curl import curl


def writer(data):
	filename = "curl_parsed.txt"
	with open(filename, "w") as f:
		for i in data:
			f.write(i + ' = ' + data[i] + '\n\n')

	print '|> Wrote to >> {}'.format(filename)


def parse_curl(curl):
	p_data = {}

	body = curl.split("--data ")[-1].replace(' --compressed', '')
	p_data['body'] = body

	url = curl.split("'")[1]
	p_data['url'] = "'" + url + "'"

	heads = {}
	headers = curl.replace(' --compressed', '').split(" --data")[0].split(" -H ")[1:]
	for header in headers:
		row = header.split(": ")
		heads[row[0].replace("'",'')] = row[1].replace("'",'')
	p_data['headers'] = json.dumps(heads,
		                           sort_keys=True,
		                           indent=4)

	cookies = {}
	cookies_data = heads['Cookie'].split('; ')
	for cookie in cookies_data:
		c_row = cookie.split("=")
		cookies[c_row[0]] = '='.join(c_row[1:])
	p_data['cookies'] = json.dumps(cookies,
		                           sort_keys=True,
		                           indent=4)

	writer(p_data)

if __name__ == '__main__':
	parse_curl(curl)