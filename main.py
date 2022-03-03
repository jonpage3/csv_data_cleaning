
import csv

master_list = []
with open('ps3500-pt-testset.csv',encoding="utf-8-sig" ) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        master_list.append(row)

#clean length field to just produce number of pages
def clean_length(book_list):
    #if 'pages' in field value process
    #else put default 100 value
    for item in book_list:
        if 'pages' in item['length']:
            print(item['length'])
        else:
            item['length'] = 100


#clean height field to just produce number in cm
def clean_height(list):
    pass

#clean date to produce year data xxxx
def clean_date(list):
    pass

#write the list into a csv file
def write_csv(list):
    pass

#clean_date(master_list)
#clean_height(master_list)
clean_length(master_list)
#write_csv(master_list)