import os
import requests_cache
import requests

from config_engine.options import BooleanOption, NumberOption, StringOption
from ipaddress import ip_interface
from typing import Union

from core.backends.base import AutonetDeviceBackend
from core.device import AutonetDevice, AutonetDeviceCredentials
from config import config

netbox_opts = [
    StringOption('url'),
    StringOption('token'),
    StringOption('private_key', default=None),
    BooleanOption('tls_verify', default=False),
    NumberOption('secret_role_id', default=1)
]

config.register_options(netbox_opts, 'netbox')


class NetBox(AutonetDeviceBackend):
    """
    Class that implements NetBox as a device backend.
    """

    def __init__(self):
        self._api = config.netbox.url + '/api'
        self._auth_header = {'Authorization': f'Token {config.netbox.token}'}
        self._private_key = config.netbox.private_key
        self.__session_key = None
        self._session = self._setup_session()
        self._session.verify = config.netbox.tls_verify

    def __str__(self):
        return f"{self.__class__.__name__}@{self._api}"

    def __repr__(self):
        return str(self)

    @staticmethod
    def _setup_session():
        """
        Determines if execution is inside the testing infrastructure.  During
        testing, it's not desirable to utilize requests_cache so the session
        object will be setup using classic requests.
        :return:
        """
        if 'PYTEST_CURRENT_TEST' in os.environ:
            return requests.Session()
        else:
            return requests_cache.CachedSession('netbox_cache', use_memory=True, expire_after=60)

    def _exec_request(self, uri, params: dict = None, headers=None,
                      json: dict = None, data: dict = None, method: str = 'GET'):
        """
        Execute a request against the NetBox API.  This helper function will
        apply all necessary headers for auth and content-type, etc.
        :param uri: NetBox API URI to call.
        :param params: URI query parameters.
        :param headers: Additional request headers.
        :param json: Payload to send as JSON.
        :param data: Payload to send as URL encoded form.
        :param method: HTTP Method.
        :return: NetBox response as `dict`.
        """
        if json or data and method == 'GET':
            raise ValueError("Cannot use `json` or `data` with GET.")
        url = f'{self._api}{uri}'
        headers = headers or {}
        headers = {**headers, **{'Accept': 'application/json'}, **self._auth_header}
        kwargs = {'headers': headers, 'params': params, 'verify': config.netbox.tls_verify}
        if json:
            kwargs['json'] = json
        if data:
            kwargs['data'] = data

        response = self._session.request(method, url, **kwargs)
        result = response.json()
        # Netbox has a standard format where the data is contained in
        # the result key except for a few endpoints.  We'll return
        # the raw result for those exceptions, and otherwise remove
        # the boilerplate from the standard responses.
        if response.status_code == 200:
            return result['results'] if 'results' in result else result
        if response.status_code == 404:
            return {}
        raise Exception("Could not parse NetBox response.")

    @property
    def _session_key(self):
        """
        The session key to be used in credential requests from secretstore plugin.
        :return:
        """
        if not self.__session_key:
            self.__session_key = self._get_session_key()
        return self.__session_key

    def _get_session_key(self):
        """
        Fetch and store the session key.
        :return:
        """
        data = {'private_key': self._private_key}
        response = self._exec_request('/plugins/netbox_secretstore/get-session-key/',
                                      data=data, method='POST')
        return response['session_key']

    def _get_device_from_netbox(self, device_id) -> dict:
        """
        Returns the device identified by `device_id`
        :param device_id:
        :return:
        """
        return self._exec_request(f'/dcim/devices/{device_id}')

    def _get_secret(self, device_id, secret_role_id: int = config.netbox.secret_role_id
                    ) -> Union[None, dict]:
        """
        Fetch a secret from the NetBox secretstore plugin.
        :param device_id: Fetch secrets for the device identified by device_id.
        :param secret_role_id: Prefer secrets assigned to this role id.
        :return:
        """
        params = {'device_id': device_id, 'limit': 0}
        headers = {'X-Session-Key': self._session_key}
        secrets = self._exec_request('/plugins/netbox_secretstore/secrets',
                                     params=params, headers=headers)
        # If there are multiple secrets, return the first one matching the configured
        # secret_role_id
        for secret in secrets:
            if secret['role']['id'] == secret_role_id:
                return secret
        # Try the only one, or none match the configured secret_role_id
        # then return the first one in the list.
        if len(secrets) == 1:
            return secrets[0]
        # Otherwise, None is returned.
        return None

    def get_device(self, device_id) -> Union[None, AutonetDevice]:
        device = self._get_device_from_netbox(device_id)
        # If we didn't find the device, just return None and let the marshalling
        # function deal with it.
        if not device:
            return None
        if not device['primary_ip4']:
            raise Exception("NetBox device has no primary_ip4 set.")
        credentials = self.get_device_credentials(device_id)
        if not credentials:
            raise Exception("Could not retrieve credentials from NetBox")
        # In classic Autonet we store metadata as k/v pairs prepended with
        # "autonet_".  Going forward this data should just be its own dictionary
        # stored in NetBox config context.   We will support both for the time being
        # and give precedence to the metadata dictionary, if it exists.
        metadata_prefix = 'autonet_'
        metadata = {k.removeprefix(metadata_prefix): v
                    for k, v in device['config_context'].items()
                    if k.startswith(metadata_prefix)}
        if 'autonet' in device['config_context']:
            metadata = {**metadata, **device['config_context']['autonet']}

        # We prefer the "driver" field but will fall back to "os"
        driver = metadata['os'] if 'os' in metadata else None
        driver = metadata['driver'] if 'driver' in metadata else driver

        return AutonetDevice(
            device_id=device_id,
            address=ip_interface(device['primary_ip4']['address']).ip,
            credentials=self.get_device_credentials(device_id),
            enabled=True if device['status']['value'] == 'active' else False,
            device_name=device['name'] or None,
            driver=driver,
            metadata=metadata
        )

    def get_device_credentials(self, device_id) -> Union[None, AutonetDeviceCredentials]:
        secret = self._get_secret(device_id)
        if secret and secret['name'] and secret['plaintext']:
            return AutonetDeviceCredentials(username=secret['name'], password=secret['plaintext'])
        else:
            return None
