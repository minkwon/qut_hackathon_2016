import cPickle as pickle
import json


def load_tag_count(tag_name, dictionary, postings_reader):
    if tag_name not in dictionary:
        return None

    postings_reader.seek(dictionary[tag_name])
    return pickle.load(postings_reader)

def get_timeline_json(tag_string):
    data = {}
    table_reader = open("static/tag_dict_position_table", "rb")
    pos_table = pickle.load(table_reader)
    table_reader.close()
    postings_reader = open("static/tag_dict_posting", "rb")

    tags = tag_string.replace(" ", "").split(",")

    # grab only the postings for user query and store in data
    for tag_name in tags:
        postings = load_tag_count(tag_name, pos_table, postings_reader)
        data[tag_name] = postings
    postings_reader.close()

    result_list = []
    month = 4
    for year in range(2009, 2017):
        while month <= 12:
            # if the data is more recent than 2016-06, ignore
            if year >= 2016 and month > 6:
                break
            # month formatting into mm, i.e) 02 for Feb, 11 for Nov
            month_s = str(month) if len(str(month)) == 2 else "0" + str(month)
            # date format is YYYY-MM
            date = str(year) + "-" + month_s
            # single entry in result list
            entry = {}
            entry['date'] = date

            # in here, the special key in data[tag] such as "total" and "earliest_record"
            # doesn't get picked up
            for tag in tags:

                #TODO: handle this properly
                # if tag wasn't found in the dictionary
                if data[tag] == None:
                    return json.dumps(["garbage"])



                elif date in data[tag]:
                    entry[tag] = data[tag][date]
                else:
                    entry[tag] = "0"
            result_list.append(entry)
            month += 1
        month = 1

    return json.dumps(result_list)


def get_home_json(query):
    data = {}
    table_reader = open("static/tag_dict_position_table", "rb")
    pos_table = pickle.load(table_reader)
    table_reader.close()
    postings_reader = open("static/tag_dict_posting", "rb")
    # grab only the postings for user query and store in data
    for tag_name in tags:
        postings = load_tag_count(tag_name, pos_table, postings_reader)
        data[tag_name] = postings
    postings_reader.close()

    result_list = []
    return None