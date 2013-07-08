"""
Calculate creatinine clearance using most recent data
"""

import cobas
import sys

CREATININE = "Kreatynina"
CREATININE_IN_URINE = 'Kreatynina w moczu'
TIMESTAMP = "Data i godzina rejestracji"

c = cobas.Server()
c.login()

plasma = urine = None

try:
    patient_name = unicode(sys.argv[1], "utf-8")
except IndexError:
    patient_name = unicode(raw_input("Patient name> "), "utf-8")


for sample in c.find_by_name(patient_name):
    badanie = c.get_single_result(sample['url'])

    if CREATININE in badanie.keys() and plasma is None:
        plasma = float(badanie[CREATININE]['value'])
        plasma_dt = sample[TIMESTAMP]

    if CREATININE_IN_URINE in badanie.keys() and urine is None:
        urine = float(badanie[CREATININE_IN_URINE]['value'])
        urine_dt = sample[TIMESTAMP]

    if urine is not None and plasma is not None:
        while True:
            try:
                ile_moczu = float(raw_input('Amount of urine (ml)> '))
                break
            except ValueError:
                pass

        while True:
            s = raw_input('Amount of hours (default=24)> ')
            if not s.strip():
                hours = 24
                break
            try:
                hours = float(s)
                break
            except ValueError:
                pass

        while True:
            try:
                weight = float(raw_input('Weight (kg)> '))
                break
            except ValueError:
                pass

        print "\tClearance:         %.2f ml/min" % (urine*ile_moczu/(plasma*hours*60))
        print "\tUrine:             %.2f ml/kg/H" % (ile_moczu/24.0/weight)
        if plasma_dt == urine_dt:
            print "\tTimestamp:        ", plasma_dt
        else:
            print "\tTimestamp urine:  ", urine_dt
            print "\tTimestamp plasma: ", plasma_dt
        break
