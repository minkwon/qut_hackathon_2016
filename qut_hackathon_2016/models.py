import cPickle as pickle
import json


def load_tag_count(tag_name, dictionary, postings_reader):
    postings_reader.seek(dictionary[tag_name])
    return pickle.load(postings_reader)

def get_tags_total_count_list():
    reader = open("/Volumes/exFat/QUT_hack/indexed_list/tag_sorted_list")
    data = json.dumps(pickle.load(reader))
    reader.close()
    return data


def get_timeline_data(tag_names):
    reader = open('/Volumes/exFat/QUT_hack/indexed_list/timeline.tsv')
    tsv = ""
    for line in reader.readlines():
        tsv += line
    return tsv