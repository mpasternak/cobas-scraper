# -*- encoding: utf-8 -*-

import requests, bs4, os
import local_settings as settings

LOGIN = '/PSMWebModule/action/DailyList/j_security_check'
SEARCH_BY_NAME = '/PSMWebModule/action/DailyList'


class CobasServer:
    def __init__(self, host, port=443):
        self.host = host
        self.port = port
        self.session = requests.Session()

    def url(self, path):
        return 'https://%s:%s/%s' % (self.host, self.port, path)

    def login(self, username, password):
        res = self.session.post(
            self.url(LOGIN), 
            auth=(username, password), 
            verify=False)
        assert(res.status_code == 200)

    def find_by_name(self, name):
        print self.session.cookies
        res = self.session.get(
            self.url(SEARCH_BY_NAME),
            params=dict(textFieldLong=name))
        assert("Zaloguj do systemu" not in res.content), "nie udało się zalogować"
        return []
        

def cobas_demo():
    c = CobasServer('192.168.0.128')
    c.login(os.getenv('COBAS_USER', settings.COBAS_USER),
            os.getenv('COBAS_PASSWORD', settings.COBAS_PASSWORD))

    print c.find_by_name('Kowalski')


if __name__ == "__main__":
    cobas_demo()
