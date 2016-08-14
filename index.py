import sys
import getopt
import nltk
import os
import math
import xml.etree.cElementTree as ET
import cPickle as pickle

"""
Returns a dictionary that maps doc ID with its document length.
Document length is the magnitude of weighted term frequency vector
generate_doc_length_table(dict<str:[int, ...]>) -> dict<int:>
"""
def generate_doc_length_table(hash_index):
    doc_length_table = {}
    for term, postings_list in hash_index.iteritems():
        for doc_id, weighted_term_frequency in postings_list:
            if doc_id in doc_length_table:
                doc_length_table[doc_id] += pow(weighted_term_frequency, 2)
            else:
                doc_length_table[doc_id] = pow(weighted_term_frequency, 2)

    for doc_id, length in doc_length_table.iteritems():
        doc_length_table[doc_id] = pow(length, 1/2)

    return doc_length_table




def index():
    tag_dict = {}

    context = ET.iterparse("/Volumes/exFat/QUT_hack/Posts.xml", events=("start", "end"))
    context_iterator = iter(context)
    event, root = context_iterator.next()
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            raw_tags = elem.attrib.get("Tags")
            year_month = elem.attrib.get("CreationDate")[:7]
            if raw_tags != None:
                tags = raw_tags[1:(len(raw_tags) - 1)].split("><")
                for tag in tags:
                    if tag not in tag_dict:
                        tag_dict[tag] = {"total" : 1, year_month : 1}
                    else:
                        tag_dict[tag]["total"] += 1
                        if year_month not in tag_dict[tag]:
                            tag_dict[tag][year_month] = 1
                        else:
                            tag_dict[tag][year_month] += 1
        # everytime it parses one xml element, the root's children is being removed to free memory
        root.clear()


    # keeping track of the earliest record of each tag
    for tag, counts in tag_dict.iteritems():
        if counts["total"] > 1000:
            print tag + " : " + str(counts["total"])
        earliest_record = ""
        for time, count in counts.iteritems():
            if time != "total":
                if earliest_record == "":
                    earliest_record = time
                else:
                    e_y, e_m = earliest_record.split("-")
                    t_y, t_m = time.split("-")
                    if int(t_y) <= int(e_y) and int(t_m) < int(e_m):
                        earliest_record = time
        tag_dict[tag]["earliest_record"] = earliest_record

    tag_dict_position_table = {}
    postings_writer = open("/Volumes/exFat/QUT_hack/indexed_list/tag_dict_posting", "wb")
    for tag, counts in tag_dict.iteritems():
        if counts["total"] > 1000:
            # current position of the file pointer
            pointer = postings_writer.tell()
            pickle.dump(counts, postings_writer)
            # each entry of dictionary: { term : (doc frequency, pointer to postings_list) }
            tag_dict_position_table[tag] = pointer

    position_table_writer = open("/Volumes/exFat/QUT_hack/indexed_list/tag_dict_position_table", "wb")
    pickle.dump(tag_dict_position_table, position_table_writer)
    postings_writer.close()
    position_table_writer.close()

index()