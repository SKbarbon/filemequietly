import os
import threading
import requests

class FileDownloader:
    def __init__(self, url, json_data, progress_handler, on_done, error_event_handler, save_as_name=None):
        """
        Initialize the FileDownloader with a URL, a progress handler, an error event handler,
        and an optional custom file name.
        
        :param url: URL of the file to download.
        :param progress_handler: Function to handle download progress (percentage of completion).
        :param error_event_handler: Function to handle errors, receives error code and exception.
        :param save_as_name: Optional custom name to save the file (including extension).
        """
        self.url = url
        self.json_data = json_data
        self.progress_handler = progress_handler
        self.error_event_handler = error_event_handler
        self.on_done = on_done
        self.save_as_name = save_as_name
        self.download_path = self._get_download_path()

    def _get_download_path(self):
        """
        Get the default Downloads folder path for the current user.
        """
        return os.path.join(os.path.expanduser("~"), "Downloads")

    def _download(self):
        """
        Internal method to download the file content and track the progress.
        """
        try:
            # Use the custom name if provided; otherwise, extract the file name from the URL
            file_name = self.save_as_name if self.save_as_name else self.url.split("/")[-1]
            file_path = os.path.join(self.download_path, file_name)

            # Stream the content to avoid loading the entire file in memory
            with requests.post(self.url, stream=True, json=self.json_data) as response:
                if response.status_code != 200:
                    raise requests.exceptions.RequestException(f"HTTP {response.status_code}")

                response.raise_for_status()  # Raise for bad responses (4xx and 5xx)
                total_size = int(response.headers.get('content-length', 0))  # Get total file size
                downloaded_size = 0

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):  # Download in chunks
                        if chunk:  # Filter out keep-alive chunks
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            progress = int((downloaded_size / total_size) * 100)
                            self.progress_handler(progress)


            self.on_done(file_path)
        except requests.exceptions.RequestException as req_err:
            error_code = getattr(req_err.response, 'status_code', None)
            self.error_event_handler(error_code, req_err)
        except Exception as e:
            self.error_event_handler(None, e)

    def start(self):
        """
        Start the download in a separate thread.
        """
        thread = threading.Thread(target=self._download, daemon=True)
        thread.start()