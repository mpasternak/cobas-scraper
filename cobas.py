# -*- encoding: utf-8 -*-

"""
Library for web scraping of data from Cobas(TM) analyzer web ui by Roche Laboratories(TM)
"""

import requests, bs4, os

ROOT = '/PSMWebModule/action'
LOGIN = ROOT + '/j_security_check'
SEARCH_BY_NAME = ROOT + '/SearchByPatientName'
SEARCH_BY_PESEL = ROOT + '/SearchByPatientID'

NOT_FOUND = 'Nie znaleziono zleceń'
PESEL_MENU = 'Szukaj po peselu'


class Server:
    def __init__(self, host='192.168.0.128', port=443):
        self.host = host
        self.port = port
        self.session = requests.Session()

    def url(self, path):
        return 'https://%s:%s%s' % (self.host, self.port, path)

    def login(self, username=None, password=None):
        try:
            import local_settings as settings
        except ImportError:
            pass

        if username is None:
            username = os.getenv('COBAS_USER', settings.COBAS_USER)

        if password is None:
            password = os.getenv('COBAS_PASSWORD', settings.COBAS_PASSWORD)

        res = self.session.get(self.url(''), verify=False)
        res = self.session.post(
            self.url(LOGIN), 
            params=dict(j_username=username, j_password=password),
            verify=False,
            headers={'content-type': 'application/x-www-form-urlencoded'})

        assert(PESEL_MENU in res.content)

    def find_by_name(self, name):
        res = self.session.get(
            self.url(SEARCH_BY_NAME),
            params=dict(name=name.encode('iso8859-2'), showAll=1))
        if NOT_FOUND in res.content:
            return
        return self.parse_name_table(res.content, width="650px")

    def parse_name_table(self, content, **extras):
        keys = []
        soup = bs4.BeautifulSoup(content)
        table = soup.find_all('table', **extras)[0]
        for n, row in enumerate(table.find_all('tr')):
            if n < 2: continue

            content = []
            url = 'url'
            for m, col in enumerate(row.find_all('td')):
                if n > 2 and m == 0:
                    url = col.find_all('a')[0]['href']

                if col.text.strip():
                    content.append(col.text.strip())
            content.append(url)
            if n == 2:
                keys = content[:]
                continue
            yield dict(zip(keys, content))

    def parse_single_result_table(self, content):
        soup = bs4.BeautifulSoup(content)
        table = soup.find_all('table', width='100%', cellspacing='0', cellpadding='0', border='0')[3]
        assert(u'Wyniki badań' in table.text)
        ret = {}
        for n, row in enumerate(table.find_all('tr')):
            values = []
            for m, col in enumerate(row.find_all('td')):
                if col.text.strip():
                    values.append(col.text.strip())

            if len(values)>=2:
                if values[0] in [u'Wyniki badań', u'Autoryzacja']:
                    continue

                ret[values[0]] = {'value': values[1]}

                if 'H' in values:
                    values.remove('H')

                if 'L' in values:
                    values.remove('L')

                if len(values)>2:
                    ret[values[0]]['units'] = values[2]

                if len(values)>3:
                    _range = values[3]

                    if _range.find(">=")>-1:
                        ret[values[0]]['range-min'] = '0'
                        ret[values[0]]['range-max'] = _range.replace(">=", "").strip()
                    else:
                        _range = _range.replace("[", "").replace("]", "").strip().split("-")
                        ret[values[0]]['range-min'] = _range[0].strip()
                        ret[values[0]]['range-max'] = _range[1].strip()

        return ret

    def find_by_pesel(self, pesel):
        res = self.session.get(
            self.url(SEARCH_BY_PESEL),
            params=dict(pid=pesel, showAll=1), verify=False)
        if PESEL_MENU not in res.content:
            print res.content
            raise Exception
        if NOT_FOUND in res.content:
            return
        return self.parse_name_table(res.content, width="650px")

    def get_single_result(self, url):
        res = self.session.get(
            self.url(url), verify=False)
        return self.parse_single_result_table(res.content)


def cobas_test():
    c = Server()
    c.login()

    print c.get_single_result('/PSMWebModule/action/ShowSingleResult?location=H&registerDate=20130513053100&view=FULL&sampleId=937828')

    for row in c.find_by_name('Kowalski'):
        print row


if __name__ == "__main__":
    cobas_test()
