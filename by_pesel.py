"""
Get patient information by patient ID
"""

import cobas
import sys

c = cobas.Server()
c.login()

for sample in c.find_by_pesel(sys.argv[1]):
    badanie = c.get_single_result(sample['url'])

    for b in badanie.keys():
        values = [sys.argv[1], sample['Data i godzina rejestracji'], sample['ID zlecenia'], b, badanie[b]['value']]
        print "\t".join([value.encode('utf-8') for value in values])