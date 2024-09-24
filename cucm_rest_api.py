import requests
import json
from bs4 import BeautifulSoup
from requests import ConnectTimeout
from requests import ConnectionError

proxies = {
    "http":"",
    "https":"",
    }
    
with open("ip_addresses.txt", 'r') as file:
    for ip_address in file:
        ip_address = ip_address.strip()
        if not ip_address.startswith("http"):
            ip_address = "http://" + ip_address
            try:
                response = requests.get(ip_address, proxies = proxies)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    device_html = soup.find('div', align="center")
                    data = { 'headings': [h.get_text() for h in  device_html.find_all(['b', 'td', 'tr'])]}
                    data_json = json.dumps(data)
                    data_json_1 =json.loads(data_json)
                    lists = ["Serial Number", "Host Name","Phone DN", "Model"]
                    new_data = []
                    for n in lists:
                        for line in data_json_1['headings']:
                            if n in line:
                                new_data.append(line)
                                break
                    final = []
                    lists_2=[" Serial Number", " Host Name", " Phone DN", " Model Number"]
                    for prefix in lists_2:
                            for item in new_data:
                                if item.startswith(prefix):
                                    item = item[len(prefix):]
                                    final.append(item)
                                    break
                    print(final)
                    

            except ConnectionError as connection_error:
                print(f"Connection error to {ip_address}: {connection_error}")
                continue
            except ConnectTimeout as timeout:
                print(f"Timeout to device {ip_address}: {timeout}")
                continue
            except Exception as unknown_error:
                print(f"Error: {unknown_error}")
                continue