"""
Calculate creatinine clearance using most recent data
"""

import cobas
import sys

CREATININE = "Kreatynina"
CREATININE_IN_URINE = 'Kreatynina w moczu'

c = cobas.Server()
c.login()

plasma = urine = None

for sample in c.find_by_name(sys.argv[1]):
    badanie = c.get_single_result(sample['url'])

    if CREATININE in badanie.keys() and plasma is None:
        plasma = float(badanie[CREATININE]['value'])

    if CREATININE_IN_URINE in badanie.keys() and urine is None:
        urine = float(badanie[CREATININE_IN_URINE]['value'])

    if urine is not None and plasma is not None:
        ile_moczu = float(raw_input('Amount of urine (ml)> '))

        try:
            hours = float(raw_input('Amount of hours (default=24)> '))
        except ValueError:
            hours = 24

        print "Clearance: %.2f ml/min" % (urine*ile_moczu/(plasma*hours*60))
        break