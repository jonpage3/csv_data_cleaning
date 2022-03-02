
import csv

master_list = []
with open('ps3000_lsc_3-2.csv',encoding="utf-8" ) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        master_list.append(row)

print(master_list)