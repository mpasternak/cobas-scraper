#!/usr/bin/env python

"""
Get patient information by patient ID

by_pesel.py [PATIENT ID]

by_pesel.py [PATIENT ID] [DATE] -- to limit to a certain date
"""

import cobas
import sys
import datetime

GODZINA_REJESTRACJI = 'Data i godzina rejestracji'

c = cobas.Server()
c.login()



try:
    date_limit = sys.argv[2]
except IndexError:
    date_limit = None

if date_limit is not None:
    try:
        y, m, d = date_limit.split('-')
    except ValueError:
        y, m, d = date_limit.split('/')

    date_limit = datetime.date(int(y), int(m), int(d))

for sample in c.find_by_pesel(sys.argv[1]):

    badanie = c.get_single_result(sample['url'])

    for b in badanie.keys():
        data, czas = sample[GODZINA_REJESTRACJI].split(" ")

        if date_limit is not None:
            y, m, d = data.split('-')
            d = datetime.date(int(y), int(m), int(d))

            if d < date_limit:
                sys.exit(0)

        values = [sys.argv[1], data, czas, sample['ID zlecenia'], b, badanie[b]['value'], badanie[b].get('units', ''),
                  badanie[b].get('material', '')]
        print "\t".join([value.encode('utf-8') for value in values])
