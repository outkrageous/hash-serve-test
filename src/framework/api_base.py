"""
api_base module for interacting with APIs
"""

import requests


class ApiBase:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def _build_url(self, endpoint, job_id=None):
        if job_id is not None:
            return f'{self.base_url}/{endpoint}/{job_id}'
        return f'{self.base_url}/{endpoint}'

    def post(self, payload, endpoint, data=None, headers=None):
        """
        Generic method executes a POST call to an API
        :param endpoint:
        :param payload: data to post (dict)
        :return: requests response object
        """
        full_url = self._build_url(endpoint)
        headers = self.headers if headers is None else headers
        response = requests.post(url=full_url, json=payload, data=data, headers=headers, verify=False)
        return response

    def get(self, endpoint, job_id=None):
        """
        Generic method executes a GET call to an API
        :return: requests response object
        """
        full_url = self._build_url(endpoint, job_id)

        response = requests.get(url=full_url, headers=self.headers, verify=False)
        return response

    def delete(self, endpoint, job_id):
        full_url = self._build_url(endpoint, job_id)
        response = requests.delete(full_url, headers=self.headers, verify=False)
        return response
