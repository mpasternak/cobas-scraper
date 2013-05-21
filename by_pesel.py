"""
Get patient information by patient ID

by_pesel.py [PATIENT ID]

by_pesel.py [PATIENT ID] [DATE] -- to limit to a certain date
"""

import cobas
import sys

GODZINA_REJESTRACJI = 'Data i godzina rejestracji'

c = cobas.Server()
c.login()



try:
    date_limit = sys.argv[2]
except IndexError:
    date_limit = None

for sample in c.find_by_pesel(sys.argv[1]):

    if date_limit:
        if sample[GODZINA_REJESTRACJI].startswith(date_limit):
            break

    badanie = c.get_single_result(sample['url'])

    for b in badanie.keys():
        values = [sys.argv[1], sample[GODZINA_REJESTRACJI], sample['ID zlecenia'], b, badanie[b]['value'], badanie[b]['units']]
        print "\t".join([value.encode('utf-8') for value in values])