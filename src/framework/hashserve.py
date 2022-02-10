from time import sleep
import psutil
import subprocess
import os

from framework.api_base import ApiBase


class HashServe:
    def __init__(self, ip='127.0.0.1', port='8088', path_to_exe='/usr/local/bin/broken-hashserve'):
        self.ip = ip
        self._port = port
        self.url = f'http://{self.ip}:{self.port}'
        self.headers = {'headers': 'application/json'}
        self.path_to_exe = path_to_exe
        self._api = None

    @staticmethod
    def _pause_after_launch_time():
        """
        Time to wait after launch before doing anything else
        :return: int
        """
        return 3

    @staticmethod
    def _pause_after_shutdown_time():
        """
        Time to wait after shutdown before doing anything else
        :return: int
        """
        return 2

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = str(port)

    @property
    def api(self):
        """Returns an instance of ApiBase"""
        if self._api is None:
            self._api = ApiBase(base_url=self.url, headers=self.headers)
        return self._api

    def launch(self):
        """Launches hashserve locally"""
        if not os.path.exists(self.path_to_exe):
            raise FileNotFoundError
        self._set_port()
        subprocess.Popen([self.path_to_exe])
        sleep(self._pause_after_launch_time())

    def _set_port(self):
        """
        Sets the port env variable
        :return:
        """
        os.environ["PORT"] = str(self.port)

    def get_stats(self):
        """
        Pull stats from the hashserve app
        :return: requests response object
        """
        response = self.api.get('stats')
        return response

    def set_password(self, password):
        """
        Post a password to hashserve for hashing
        :param password: Password to hash
        :return: requests response object
        """
        data = {'password': password}
        response = self.api.post(payload=data, endpoint='hash')
        return response

    def get_password_hash(self, job_id):
        """
        Get the hash of a password by job id
        :param job_id: job id
        :return: requests response object
        """
        response = self.api.get('hash', job_id)
        return response

    def delete_by_id(self, job_id):
        """
        Delete a hash by id

        Note: This is not currently a feature of hashserve
        :param job_id: job id of hash
        :return: requests response object
        """
        return self.api.delete('hash', job_id)

    def shutdown(self):
        """
        Send shutdown command to hashserve
        :return: requests response object
        """
        return self.api.post(payload=None, endpoint='hash', data='shutdown')

    def shutdown_if_running(self):
        """
        Check if the app is running locally and send shutdown command if it is
        :return: Returns true if successful
        """
        if self.is_hashserve_running():
            response = self.api.post(payload=None, endpoint='hash', data='shutdown')

            if not response.ok:
                raise Exception(f"Shutdown encountered an error {response.json()}")
        else:
            print('Hashserve not found to be running')

        return True

    @staticmethod
    def is_hashserve_running():
        """
        Detects if hashserve is running locally
        :return: bool
        """
        process_name = 'broken-hashserve'
        for proc in psutil.process_iter():
            return proc.name() == process_name
        return False

    def refresh_hashserve(self):
        """
        Shuts down hashserve if it's running and then launches it
        :return:
        """
        self.shutdown_if_running()
        self.launch()
