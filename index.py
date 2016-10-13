import sys
import getopt
import nltk
import os
import math
import xml.etree.cElementTree as ET
import cPickle as pickle
import time


if __name__ == "__main__":
    
    startTime = time.time()
    tag_dict = {}

    context = ET.iterparse("/Volumes/exFat/QUT_hack/Posts.xml", events=("start", "end"))
    context_iterator = iter(context)
    event, root = context_iterator.next()
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            raw_tags = elem.attrib.get("Tags")
            year_month = elem.attrib.get("CreationDate")[:7]
            if raw_tags != None:
                # tags looks like "<linux><ubuntu><bash>"
                tags = raw_tags[1:(len(raw_tags) - 1)].split("><")
                for tag in tags:
                    if tag not in tag_dict:
                        # init counts dictionary
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
    postings_writer = open("static/tag_dict_posting", "wb")
    for tag, counts in tag_dict.iteritems():
        # only save tags that have more than 1000 total counts
        if counts["total"] > 1000:
            # current position of the file pointer
            pointer = postings_writer.tell()
            pickle.dump(counts, postings_writer)
            # each entry of dictionary: { term : (doc frequency, pointer to postings_list) }
            tag_dict_position_table[tag] = pointer

    position_table_writer = open(" static/tag_dict_position_table", "wb")
    pickle.dump(tag_dict_position_table, position_table_writer)
    postings_writer.close()
    position_table_writer.close()

    endTime = time.time()

    print "Time taken: " + (endTime - startTime) "seconds"