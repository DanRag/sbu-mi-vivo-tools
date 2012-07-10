__author__ = 'janos'

from wok_util import author_process_full as author_process

codes_map = {"FN" : "Format",
 "VR" : "",
 "PT" : None,
 "AU" : "authors",
 "TI" : "title",
 "SO" : "title",
 "VL" : "volume",
 "IS" : "issue",
 "PD" : "publication date",
 "PY" : "year",
 "AB" : "abstract",
 "SN" : "issn",
 "UT" : "identifier",
 "DI" : "doi",
 "AB" : "abstract",
 "UT" : "identifier",
 "BP" : "start_page",
 "EP" : "end_page"
 }
source_codes = ["SO","VL","PY","PD","SN","BP","EP"]

import re

def convert_record_json_readable(records):
    new_record_list = []
    for record in records:
        new_record = convert_format_to(record)
        if len(new_record.keys()):
            new_record_list.append(new_record)
    return new_record_list

def convert_format_to(record):
    converted_structure = {}

    if "AU" in record:
        processed_author_list = []
        authors = record["AU"]
        for author in authors:
            processed_author_list.append(author_process(author))
        converted_structure[codes_map["AU"]] = processed_author_list

    return converted_structure



def read_format(text, new_record_marker = "PT", list_entries = ["AU"]):

    regex_start_record = re.compile("^([A-Z][A-Z0-9])")
    records = []
    record = {}

    field_match = None
    i = 0
    value_string = ""
    split_lines = text.split("\n")

    for line in split_lines:
        match_result = regex_start_record.match(line)
        if match_result:

            last_field_match = field_match
            field_match = match_result.group().strip()

            if '||' in value_string:
                record[last_field_match] = value_string.split("||")
            else:
                record[last_field_match] = [value_string]

            value_string = line[3:].strip()

            if field_match == new_record_marker:
                records.append(record)
                record = {}
        else:
            if value_string:
                if value_string[-1] == "-":
                    pass
                elif field_match in list_entries:
                    value_string += "||"
                else:
                    value_string += " "

                value_string += line[3:].strip()
    i += 1
    if len(record.keys()):
        records.append(record)
    return records

if __name__ == "__main__":
    import pprint
    f = open("test/export_wok.txt")
    parsed_format = read_format(f.read())

    json_friendly_format = convert_record_json_readable(parsed_format)
    pprint.pprint(json_friendly_format)


    sample_record = """
PT J
AU Hajagos, Janos G.
TI Interval Monte Carlo as an alternative to second-order sampling for
   estimating ecological risk
SO RELIABLE COMPUTING
VL 13
IS 1
BP 71
EP 81
DI 10.1007/s11155-006-9019-0
PD FEB 2007
PY 2007
AB Interval Monte Carlo offers an alternative to second-order approaches
   for modeling measurement uncertainty in a simulation framework. Using
   the example of computing quasi-extinction decline risk for an ecological
   population, an interval Monte Carlo model is built. If the model is not
   written optimally, the mean and standard deviation of the growth rate
   repeat, then the bounds on the quasi-extinction risk will be
   sub-optimal. Depending on your operational definition of what an
   interval is, the sub-optimal bounds may be the best possible bounds. A
   comparison between second-order and interval Monte Carlo is made, which
   reveals that second-order approaches can underestimate the upper bound
   on the quasi-extinction decline risk to the population when there are a
   large number of parameters that need to be sampled.
TC 1
Z9 1
SN 1385-3139
UT WOS:000252216100003
ER"""
