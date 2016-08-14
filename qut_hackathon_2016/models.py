import cPickle as pickle
import json


def load_tag_count(tag_name, dictionary, postings_reader):
    reader = open("/Volumes/exFat/QUT_hack/indexed_list/tag_dict_posting", "rb")
    postings_reader.seek(dictionary[term][1])
    return pickle.load(postings_reader)

def get_tags_total_count_list():
    reader = open("/Volumes/exFat/QUT_hack/indexed_list/tag_sorted_list")
    data = json.dumps(pickle.load(reader))
    print data
    return data