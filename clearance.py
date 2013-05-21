"""
Calculate creatinine clearance using most recent data
"""

import cobas
import sys

CREATININE = "Kreatynina"
CREATININE_IN_URINE = 'Kreatynina w moczu'

c = cobas.Server()
c.login()

for sample in c.find_by_name(sys.argv[1]):
    badanie = c.get_single_result(sample['url'])

    if CREATININE in badanie.keys() and CREATININE_IN_URINE in badanie.keys():
        ile_moczu = float(raw_input('Amount of urine (ml)> '))

        try:
            hours = float(raw_input('Amount of hours (default=24)> '))
        except ValueError:
            hours = 24

        plasma = float(badanie[CREATININE]['value'])
        urine = float(badanie[CREATININE_IN_URINE]['value'])

        print "Clearance: %.2f ml/min" % (urine*ile_moczu/(plasma*hours*60))
        break