import re
import os

import requests

from utils.singleton import Singleton

REPO_BASE = '%s' % os.getenv('REPO_SERVER')


class Repository(Singleton):

    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True

    def __get_json(self, path):
        url = '%s%s' % (REPO_BASE, path)
        r = requests.get(url)

        return r.json()

    def query(self, package, commit):
        path = '/package/%s' % package
        r = self.__get_json(path)
        package_list = []

        if r.get('failed'):
            raise Exception('sub-system(repo-server) error: %s' % r.get('result'))

        for p in r.get('result'):
            v = p.get('version')
            r = re.compile('[\d\.]+\+r\w+~g(.+)')
            l = r.findall(v)

            if len(l) == 0:
                continue

            pkg_comm_hash = l[0]
            if not commit.startswith(pkg_comm_hash):
                continue

            package_list.append(p)

        return package_list
