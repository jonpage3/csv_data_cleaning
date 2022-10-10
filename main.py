
import csv
import re
import random
import add_random_color
from nltk.corpus import stopwords

# Default values
# height: 20
# length: 100
# date: 1950
# min_length: 30
DEFAULT_HEIGHT = 20
DEFAULT_LENGTH = 100
DEFAULT_DATE = 1950
DEFAULT_MIN_LENGTH = 30

master_list = []
with open('ps3500-pt-testset.csv', encoding="utf-8-sig",errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        master_list.append(row)


# not used
# clean length field to just produce number of pages
def clean_length(book_list):
    # if 'pages' in field value process
    # else put default 100 value
    for item in book_list:
        if 'pages' not in item['length']:
            item['clean_length'] = DEFAULT_LENGTH
            # print("we changed this one")
            # print(item['callnum'])
        else:
            s = item['length']
            s_list = re.findall(r"(\d+) pages", s)
            try:
                item['clean_length'] = int(max(s_list))
            except ValueError:
                s_list = re.findall(r"(\d+) unnumbered pages", s)
                try:
                    item['clean_length'] = int(max(s_list))
                except ValueError:
                    s1 = re.split(r"[\b\W\b]+", s)
                    numlist = []
                    for x in s1:
                        try:
                            numlist.append(int(x))
                        except ValueError:
                            pass
                    if len(numlist) > 0:
                        item['clean_length'] = max(numlist)
                    else:
                        item['clean_length'] = DEFAULT_LENGTH


# clean height field to just produce number in cm
def clean_height(book_list):
    # if 'cm' in field value process
    # else put default 20 value
    for item in book_list:
        if 'cm' not in item['height']:
            item['clean_height'] = DEFAULT_HEIGHT
        else:
            s = item['height']
            s_split = re.split(r"[\b\W\b]+", s)
            numlist = []
            for x in s_split:
                try:
                    numlist.append(int(x))
                except ValueError:
                    pass
            if len(numlist) > 0:
                item['clean_height'] = max(numlist)
            else:
                item['clean_height'] = DEFAULT_HEIGHT
        if item['clean_height'] > 50:
            item['clean_height'] = DEFAULT_HEIGHT


# clean date to produce year data xxxx
def clean_date(book_list):
    for item in book_list:
        # print(item['callnum'])
        # print(len(item['date']))
        if len(item['date']) == 0 and len(item['vol']) == 0:
            s = item['callnum']
            call_split = s.split(' ')
            try:
                item['clean_date'] = int(call_split[-1])
            except ValueError:
                item['clean_date'] = DEFAULT_DATE
        elif len(item['date']) == 0 and len(item['vol']) > 0:
            s = item['vol']
            s_split = re.split(r"[\b\W\b]+", s)
            numlist = []
            for x in s_split:
                try:
                    numlist.append(int(x))
                except ValueError:
                    pass
            if len(numlist) > 0 and max(numlist) > 1000:
                item['clean_date'] = max(numlist)
            else:
                item['clean_date'] = DEFAULT_DATE
            # print(item['callnum'])
            # print(item['clean_date'])
        else:
            s = item['callnum']
            call_split = s.split(' ')
            try:
                item['clean_date'] = int(call_split[-1])
            except ValueError:
                s_vol = item['vol']
                if len(s_vol) > 0:
                    vol_split = re.split(r"[\b\W\b]+", s_vol)
                    vnum_list = []
                    for x in vol_split:
                        try:
                            vnum_list.append(int(x))
                        except ValueError:
                            pass
                    if len(vnum_list) > 0 and max(vnum_list) > 1000:
                        item['clean_date'] = max(vnum_list)
                    else:
                        s_date = item['date']
                        s_d = re.split(r"[\b\W\b]+", s_date)
                        sdl = []
                        for i in s_d:
                            try:
                                sdl.append(int(i))
                            except ValueError:
                                pass
                        if len(sdl) > 0:
                            item['clean_date'] = max(sdl)
                        else:
                            j = max(s_d)
                            item['clean_date'] = int(j[1:])

                else:
                    s_date = item['date']
                    # print(item['date'])
                    s_d = re.split(r"[\b\W\b]+", s_date)
                    # print(s_d)
                    sdl = []
                    for i in s_d:
                        try:
                            sdl.append(int(i))
                        except ValueError:
                            pass
                    if len(sdl) > 0 and max(sdl) > 1000:
                        item['clean_date'] = max(sdl)
                        # print(item['clean_date'])
                    else:
                        j = max(s_d)
                        try:
                            date_num = int(j[1:])
                            if date_num > 1000:
                                item['clean_date'] = date_num
                            else:
                                item['clean_date'] = DEFAULT_DATE
                        except ValueError:
                            item['clean_date'] = DEFAULT_DATE


# write the list into a csv file
def write_csv(booklist):
    with open('clean_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['callnum', 'vol', 'checkouts', 'title', 'title2', 'author','pub_location','publisher','date',
                      'length', 'height', 'contents', 'subjects','subjects2','clean_date','clean_height','clean_length','color','id','clean_author','keyword_string','callnum_string','font_family','clean_title']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # use this to iterate through list of dictionaries
        writer.writeheader()
        for elem in booklist:
            writer.writerow(elem)


def new_clean_length(booklist):
    for item in booklist:
        if len(item['length']) == 0:
            item['clean_length'] = DEFAULT_LENGTH

        # have to do special things for those items with volume
        elif len(item['length']) > 0 and 'vol' in item['length']:
            # print(item['length'])
            if 'pages' in item['length'] and re.search("[0-9] vol", item['length']):

                # to handle specific weirdness
                s = re.split(r'[^a-zA-Z0-9]', item['length'])
                # count how many times pages appears in description
                pages_count = [1 for p in s if "pages" in p]
                if len(pages_count) > 1:
                    n = 0
                    page_total = 0
                    while n < len(s):
                        if 'pages' in s[n] or 'unnumbered' in s[n]:
                            try:
                                page_total += int(s[n-1])
                            except ValueError:
                                pass
                        n += 1
                    pnum = []
                    for i in s:
                        try:
                            pnum.append(int(i))
                        except ValueError:
                            pass
                    item['clean_length'] = int(page_total/min(pnum))
                else:
                    pnum = []
                    for i in s:
                        try:
                            pnum.append(int(i))
                        except ValueError:
                            pass

                    item['clean_length'] = int(max(pnum)/min(pnum))

            # volume isn't clearly indicated but page numbers are
            elif 'pages' in item['length'] and not re.search("[0-9] vol", item['length']):
                plist = re.split(r"[\b\W\b]+", item['length'])
                pnum = []
                for i in plist:
                    try:
                        pnum.append(int(i))
                    except ValueError:
                        pass
                item['clean_length'] = max(pnum)

            else:
                # no clear indication of page length
                item['clean_length'] = DEFAULT_LENGTH

        else:
            # print(item['length'])
            s = re.split(r'[^a-zA-Z0-9]', item['length'])
            pages_count = [1 for p in s if "pages" in p]
            if len(pages_count) > 1:
                n = 0
                page_total = 0
                while n < len(s):
                    if 'pages' in s[n] or 'unnumbered' in s[n]:
                        try:
                            page_total += int(s[n - 1])
                        except ValueError:
                            pass
                    n += 1
                pnum = []
                for i in s:
                    try:
                        pnum.append(int(i))
                    except ValueError:
                        pass

                if len(pnum) > 1:
                    item['clean_length'] = page_total
                # this works fine
                else:
                    item['clean_length'] = pnum[0]
            else:
                pnum = []
                for i in s:
                    try:
                        pnum.append(int(i))
                    except ValueError:
                        pass
                if len(pnum) > 0:
                    item['clean_length'] = int(max(pnum))
                else:
                    item['clean_length'] = DEFAULT_LENGTH

        # set a default min length to help with visualization
        if item['clean_length'] < 30:
            item['clean_length'] = DEFAULT_MIN_LENGTH

# extremely basic generation of hex colors
def add_color(book_list):
    golden_ratio_conjugate = 0.618033988749895

    for item in book_list:
        h = float(f'{random.random():.17f}')
        h += golden_ratio_conjugate
        h %= 1
        # color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        item['color'] = add_random_color.hslToRgb(h, 0.5, 0.40)


# basic functionality, should be adjusted after getting Sierra item records
def add_id(book_list):
    acc = 1
    for item in book_list:
        item['id'] = acc
        acc += 1


# add a clean author field to help with author searching
def clean_author(book_list):
    for item in book_list:
        author = item['author']
        author = re.sub(r'http\S+', '', author)

        author = author.replace(' author.', '')
        # print(author)
        author = re.sub("[^A-Za-z]", "", author)
        author = author.lower()
        item['clean_author'] = author
        # print(author)

# add a string that can be used for keyword search
def create_keyword_string(book_list):
    stopwords_pattern = re.compile(r'\b(' + r'|'.join(stopwords.words()) + r')\b\s*')
    for item in book_list:
        keyword_string = item['title'] + item['title2'] + item['clean_author'] + item['pub_location'] + item['publisher'] + item['contents'] + item['subjects'] + item['subjects2']
        keyword_string = re.sub(r'http\S+', '', keyword_string)
        keyword_string = stopwords_pattern.sub('',keyword_string)
        keyword_string = re.sub("[^A-Za-z]", "", keyword_string)
        keyword_string = keyword_string.lower()
        item['keyword_string'] = keyword_string

def create_callnum_string(book_list):
    for item in book_list:
        callnum = item['callnum']
        callnum = re.sub("[^A-Za-z0-9]", "", callnum)
        callnum = callnum.lower()
        item['callnum_string'] = callnum

def add_font_family(book_list):
    for item in book_list:
        date = item['clean_date']
        if date in range(0,1850):
            item['font_family'] = 'Baskervville'
        elif date in range(1850,1875):
            item['font_family'] = 'Libre Caslon Text'
        elif date in range(1875,1900):
            item['font_family'] = 'Space Grotesk'
        elif date in range(1900,1925):
            item['font_family'] = 'Goudy Bookletter 1911'
        elif date in range(1925,1950):
            item['font_family'] = 'Times New Roman'
        elif date in range(1950,1975):
            item['font_family'] = 'Helvetica'
        elif date in range(1975,2000):
            item['font_family'] = 'Lucida Console'
        elif date in range(2000,2025):
            item['font_family'] = 'MuseoModerno'
        else:
            item['font_family'] = "sans-serif"

def clean_title(book_list):
    for item in book_list:
        title = item['title']
        if title[-1:].isalnum():
            item['clean_title'] = title
        else:
            item['clean_title'] = title[:-1]


# run the program

clean_date(master_list)
clean_height(master_list)
new_clean_length(master_list)
add_color(master_list)
add_id(master_list)
clean_author(master_list)
create_keyword_string(master_list)
create_callnum_string(master_list)
add_font_family(master_list)
clean_title(master_list)
write_csv(master_list)





