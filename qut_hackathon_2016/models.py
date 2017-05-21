import pickle
import json


def load_posting_by_key(key, dictionary, postings_reader):
    if key not in dictionary:
        return None
    print(dictionary[key])
    postings_reader.seek(dictionary[key])
    return pickle.load(postings_reader)


def get_question_data_for_tag(tags):
    result = {}
    table_reader = open("static/questions_position_table", "rb")
    pos_table = pickle.load(table_reader)
    table_reader.close()
    postings_reader = open("static/questions_postings", "rb")

    # "former" : {
    #   "name : "java",
    #   "series" : [{
    #       "date" : "2013-4",
    #       "data" : [Q's, #Q'sWithAnswer, #Q'sWithAcceptedAnswer, timeForFirstAnswer, timeForAcceptedAnswer]
    #   }, {...}],
    # "latter" : {
    #   "name : "c",
    #   "series" : [{
    #       "date" : "2013-4",
    #       "data" : [Q's, #Q'sWithAnswer, #Q'sWithAcceptedAnswer, timeForFirstAnswer, timeForAcceptedAnswer]
    #   }, {...}]
    # }

    former_data = load_posting_by_key(tags["former"].lower(), pos_table, postings_reader)
    former = {"name": tags["former"], "series": []}
    for date, data in former_data.items():
        former["series"].append({"date": date, "data": data})

    latter_data = load_posting_by_key(tags["latter"].lower(), pos_table, postings_reader)
    latter = {"name": tags["latter"], "series": []}
    for date, data in latter_data.items():
        latter["series"].append({"date": date, "data": data})

    result["former"] = former
    result["latter"] = latter
    postings_reader.close()
    return result


def get_timeline_json(tag_string):
    data = {}
    table_reader = open("static/tag_dict_position_table", "rb")
    pos_table = pickle.load(table_reader)
    table_reader.close()
    postings_reader = open("static/tag_dict_posting", "rb")

    tags = tag_string.replace(" ", "").split(",")

    # grab only the postings for user query and store in data
    for tag_name in tags:
        postings = load_posting_by_key(tag_name, pos_table, postings_reader)
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
            entry = {'date': date}

            # in here, the special key in data[tag] such as "total" and "earliest_record"
            # doesn't get picked up
            for tag in tags:

                # TODO: handle this properly
                # if tag wasn't found in the dictionary
                if data[tag] is None:
                    return json.dumps([])
                elif date in data[tag]:
                    entry[tag] = data[tag][date]
                else:
                    entry[tag] = "0"
            result_list.append(entry)
            month += 1
        month = 1

    return json.dumps(result_list)


def get_home_json(query):
    table_reader = open("static/tag_dict_position_table", "rb")
    pos_table = pickle.load(table_reader)
    table_reader.close()
    postings_reader = open("static/tag_dict_posting", "rb")

    result_list = []
    if query == 'totalCount':
        # grab all the postings
        for tag_name, position in pos_table.items():
            entry = {}
            postings = load_posting_by_key(tag_name, pos_table, postings_reader)
            entry["tagName"] = tag_name
            entry["totalCount"] = postings["total"]
            result_list.append(entry)
        postings_reader.close()

    result_list.sort(key=lambda entry: entry["totalCount"], reverse=False)
    return json.dumps(result_list)


def get_tags():
    return tag_list


p_reader = open("static/questions_position_table", "rb")
tag_list = []
count = 0
tag_dict = pickle.load(p_reader)
p_reader.close()
for tag, pos in tag_dict.items():
    tag_list.append(tag)
