# -*- coding: utf-8 -*-
from rich import print
from os.path import join, expanduser, isfile
from host_tools import File

from .Proxy import Proxy


class ProxyFile:
    _checked_files = {}
    _default_proxy_file = join(expanduser('~'), '.telegram', 'proxy.json')

    def __init__(self, path: str = None):
        self._proxy_file = self._get_proxy_file(path)


    def _get_proxy_file(self, path: str = None) -> str:
        if path and isinstance(path, str) and isfile(path):
            return path
        elif isfile(self._default_proxy_file):
            return self._default_proxy_file
        print(f"[red]Proxy configuration file not found")

    def get_configs(self) -> dict:
        result = {}
        file_key = self._proxy_file if self._proxy_file else 'None'

        if self._proxy_file:
            if file_key in ProxyFile._checked_files:
                return ProxyFile._checked_files[file_key]

            config = File.read_json(self._proxy_file)
            if self._check_config(config):
                proxy = Proxy(login=config['login'], password=config['password'], ip=config['ip'], port=config['port'])
                result = proxy.configs

        ProxyFile._checked_files[file_key] = result

        return result

    @staticmethod
    def _check_config(config: dict) -> bool:
        for key in ['login', 'password', 'ip', 'port']:
            if not config.get(key, None):
                print(f"[red]|ERROR| Empty parameter {key} in proxy.json file")
                return False
        return True
