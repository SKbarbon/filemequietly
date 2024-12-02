from urllib.parse import urljoin
import requests, json



class GetHostInfo:
    def __init__(self, host_link:str):
        full_link = urljoin(host_link, "host_information")
        r = requests.get(full_link)

        resp = json.loads(r.text)

        self.file_name = resp['file_name']
        self.post_download_message = resp['post_download_message']
        self.download_file_url = urljoin(host_link, "download_file")