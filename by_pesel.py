import cobas
import sys

c = cobas.Server()
c.login()

for sample in c.find_by_pesel(sys.argv[1]):
    badanie = c.get_single_result(sample['url'])

    for b in badanie.keys():
        print sys.argv[1], '\t', sample['Data i godzina rejestracji'], '\t', sample['ID zlecenia'], '\t', b, '\t', badanie[b]['value']