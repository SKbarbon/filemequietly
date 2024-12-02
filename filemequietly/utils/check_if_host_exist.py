from urllib.parse import urljoin
import requests, json



def check_if_host_exist (host_link:str) -> bool:
    full_link = urljoin(host_link, "host_information")

    try:
        r = requests.get(full_link)
        resp = json.loads(r.text)
        if resp['ok'] and resp['host_active']:
            return True
        else:
            return False
    except:
        return False