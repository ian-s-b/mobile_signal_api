"""File containing the ApiAdresse class."""
from logging import Logger
from typing import Dict
from pathlib import Path
import requests


class ApiAdresse:
    """Class used to make requests to the 'API adresse'."""
    def __init__(self, logger: Logger, base_url: str = "https://api-adresse.data.gouv.fr") -> None:
        """
        Initialize the ApiAdresse class.

        :param logger: Logger object.
        :param base_url: Url of the API endpoint.
        :return: None.
        """
        self._logger = logger
        self._base_url = base_url

    def search(self, query: str, timeout: str) -> Dict:
        """
        Make a get request to the 'API adresse' 'search' endpoint.
        Api limitations: 50 request by second for the same IP.

        :param query: the address query.
        :param timeout: Timeout for the request.
        :return: The response of the request.
        """
        endpoint = self._base_url + "/search"
        data = None
        params = {'q': query}

        try:
            response = requests.get(endpoint, params=params, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                self._logger.debug(f"Data fetched correctly. Status code: {response.status_code}")
            else:
                self._logger.error(f"Failed to fetch data. Status code: {response.status_code}")

        except requests.Timeout:
            self._logger.error("Request timed out.")

        except requests.RequestException as exception:
            self._logger.error(f"Request error: {exception}.")

        return data

    def reverse_csv(self, csv_file: Path, timeout: str) -> Dict:
        """
        Make a get request to the 'API adresse' 'search csv' endpoint.

        :param csv_file: path to csv input file.
        :param timeout: timeout for the request.
        :return: The response of the request.
        """
        endpoint = self._base_url + "/reverse/csv/"
        data = None

        try:
            with open(csv_file, 'rb') as file:
                files = {'data': file}
                response = requests.post(endpoint, files=files, timeout=timeout)

            if response.status_code == 200:
                data = response.content
                self._logger.debug(f"Data fetched correctly. Status code: {response.status_code}")
            else:
                self._logger.error(f"Failed to fetch data. Status code: {response.status_code}")

        except requests.Timeout:
            self._logger.error("Request timed out.")

        except requests.RequestException as exception:
            self._logger.error(f"Request error: {exception}.")

        return data
