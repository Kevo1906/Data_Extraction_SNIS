import requests
import time
import traceback
import os
import urllib
import mimetypes
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException
import shutil
import warnings
from datetime import datetime
from collections import defaultdict
from download_tools import createDirectoryStruct, get_proxy, format_date

class Download_Base():
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
            }
    
    def verify_url(self,url, retries=3, wait_time=3, timeout=120, is_download_url=False):
        """
        Check if the main URL is accessible.

        Arguments:
            url (string): URL to verify.
            retries (int): Number of retries.
            wait_time (int): Wait time between retries.
            timeout (int): Request timeout.

        Returns:
            bool: True if reachable, False if not reachable.
        """
        
        # Create a session to maintain state across multiple requests
        session = requests.Session()

        # Create an HTTPAdapter with maximum retries
        adapter = HTTPAdapter(max_retries=retries)

        # Mount the adapter to both HTTP and HTTPS protocols
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # Iterate over retries
        for _ in range(retries):
            try:
                # Ignore Unverified HTTPS request warning
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    # Send a GET request to the URL with stream=True, timeout, and SSL verification disabled
                    response = session.get(
                        url, stream=True, timeout=timeout, verify=False, headers=self.headers)

                    # If response status code is 403 (Forbidden), try with a random proxy
                    if response.status_code == 403:
                        random_proxy = get_proxy()
                        response = session.get(
                            url,
                            stream=True,
                            timeout=timeout,
                            verify=False,
                            proxies={
                                'http': random_proxy['proxy'],
                                'https': random_proxy['proxy']},
                            headers=self.headers)

                    # Check if the response status code indicates success (2xx range)
                    if 200 <= response.status_code < 300:
                        # Check if the URL is a download URL by inspecting the content-type header
                        if is_download_url:
                            mime_type = mimetypes.guess_extension(response.headers['content-type'])
                            parsed_url = urllib.parse.urlparse(url)
                            file_name = os.path.basename(parsed_url.path)
                            extension = os.path.splitext(file_name)[1]
                            if mime_type or extension:
                                print(f"{response.url} is reachable download url, a succesful response")
                                return True
                            else:
                                print(f"{response.url} is not a download url")
                                return False
                        print(f"{response.url} is reachable, a successful response.")
                        return True
                    else:
                        # Print error message if status code indicates failure
                        print(f"{response.url} is not reachable, status_code: {response.status_code}")
                        return False
            except ConnectionError as e:
                # Handle ConnectionError exception
                print(f"Connection error: {e}")
            except Timeout as e:
                # Handle Timeout exception
                print(f"Timeout error: {e}")
                return False
            except TooManyRedirects as e:
                # Handle TooManyRedirects exception
                print(f"Too many redirects: {e}")
                return False
            except RequestException as e:
                # Handle other RequestException exceptions
                print(f"Request exception: {e}")
                return False

            # If an exception occurred, wait for a specified time before retrying
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        # Return False if all retries are exhausted
        return False


    def store_new_data(self, path, tmp_path,last_file_path, ALL=False,format='%Y-%m-%d'):
        """
        Store new data files by comparing with existing files.

        Parameters:
        path (str): Base path for the new data files.
        tmp_path(str): Path when the temporary files were downloaded
        last_file_path (str): Path to the directory containing the last set of files.
        format (str): Date format used in the file names. Default is '%Y-%m-%d'.
        ALL(bool): Boolean variable to decide if the files we are going to be compared or not

        Returns:
        list: A list of dictionaries containing the download URL, the date to which data is updated, and the file path.
        """
        try:
            print("Starting the process of storing new data files...")
            files_to_store = []
            if ALL:
                files_to_store = os.listdir(tmp_path)
                
            else :
                # Get list of last files and group them by file code
                last_files = os.listdir(last_file_path)
                last_files_dict = defaultdict(list)
                for f in last_files:
                    f_name = os.path.splitext(f)[0]
                    f_code = f_name[10:]
                    last_files_dict[f_code].append(f) 

                # Process new files in the temporary directory
                for file in os.listdir(tmp_path):
                    file_name = os.path.splitext(file)[0]
                    file_date = format_date(file_name[:10])
                    file_code = file_name[10:]

                    # Retrieve last files with the same file code
                    last_file = last_files_dict.get(file_code, [])
                    if not last_file:
                        files_to_store.append(file)
                        continue

                    # Check if the current file is not the latest
                    is_latest = any(file_date <= format_date(os.path.splitext(f)[0][:10]) for f in last_file)
                    if not is_latest:
                        files_to_store.append(file)
                        continue
            
            # If no new files to store, return an empty list
            if not files_to_store:
                print("There is no new data to store.")
                return[]
            
            # Determine the latest date from the new files to store
            if ALL:
                last_date = datetime.today().strftime(format=format)
            else:
                last_date = max(files_to_store)[:10]

             # Create directory structure for the new files
            new_file_path = createDirectoryStruct(
                file_date=last_date,
                base_path=path,
                publication_frequency="diario"
            )
            new_file_path = os.path.join(new_file_path,last_date)
            if not os.path.exists(new_file_path):
                os.makedirs(new_file_path)
            
            # Copy new files to the new directory
            for file in files_to_store:
                src_path = os.path.join(tmp_path,file)
                dest_path = os.path.join(new_file_path,file)
                if os.path.isfile(src_path):
                    shutil.copy(src_path,dest_path)
                elif os.path.isdir(src_path):
                    for index,f in enumerate(os.listdir(src_path)):
                        shutil.copy(os.path.join(src_path,f),f"{dest_path}_dirfile{index}")
                else:
                    raise ValueError(f"There is an error with the file: {file}")
            print(f"There are {len(files_to_store)} new files stored successfully.")

            return [{
                "download_url": "-",
                "updated_to": last_date,
                "datax_file_path": new_file_path
            }]
        
        except Exception as e:
            print(f"An error ocurred: {e}")
            traceback.print_exc()
            return []