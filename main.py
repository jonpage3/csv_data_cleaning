
import csv

master_list = []
with open('ps3500-pt-testset.csv',encoding="utf-8-sig" ) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        master_list.append(row)

print(master_list)