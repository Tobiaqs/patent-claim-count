import csv
import sys
import re
import datetime
import google_patent_scraper
import json

csv.field_size_limit(sys.maxsize)

with open('combined.txt', encoding='utf-16-le') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')

    scraper = google_patent_scraper.scraper_class()
    i = 0
    rows = []
    for row in reader:
        rows.append(row)
        patent_numbers = re.findall("(US[0-9]+)", row['\ufeffPN '])
        patent_number = patent_numbers[0]
        for s in patent_numbers[1:]:
            if len(s) < len(patent_number):
                patent_number = s
        if len(patent_number) > 10:
            continue
        scraper.add_patents(patent_number)
        i += 1
        #if i == 5:
        #    break
    
    scraper.scrape_all_patents()

    pp = scraper.parsed_patents

    if len(pp) < 10:
        print("pp small")
    
    for app_no in scraper.parsed_patents:
        patent = scraper.parsed_patents[app_no]
        got = False
        for row in rows:
            if app_no in row['\ufeffPN ']:
                print("yay")
                got = True
                row["CC"] = patent["claims_count"]
                row["FCN"] = len(patent["forward_cite_no_family"])
                row["FCY"] = len(patent["forward_cite_yes_family"])
                print(row["CC"])
                print(row["FCN"])
                print(row["FCY"])
        if not got:
            print("noooooooo")

with open('mod.txt', 'wt') as tsvfile:
    tsv_writer = csv.writer(tsvfile, dialect='excel-tab')
    
    tsv_writer.writerow(reader.fieldnames + ["CC", "FCN", "FCY"])
    for row in rows:
        flat_row = []
        for header in reader.fieldnames + ["CC", "FCN", "FCY"]:
            if not header in ["CC", "FCN", "FCY"] or header in row:
                flat_row.append(row[header])
        tsv_writer.writerow(flat_row)
