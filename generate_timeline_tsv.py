import cPickle as pickle

def load_tag_count(tag_name, dictionary, postings_reader):
    postings_reader.seek(dictionary[tag_name])
    return pickle.load(postings_reader)

def generate_timeline_tsv(tag_string):
    data = {}
    # comma separated values 
    tag_names = tag_string

    table_reader = open("static/tag_dict_position_table", "rb")
    pos_table = pickle.load(table_reader)
    table_reader.close()
    postings_reader = open("static/tag_dict_posting", "rb")
    for tag_name in tag_names.split(","):
        postings = load_tag_count(tag_name, pos_table, postings_reader)
        data[tag_name] = postings
    postings_reader.close()

    tab_label = "date\t" + tag_names.replace(",", "\t")
    tags = tag_names.split(",")
    with open ('static/timeline.tsv','w') as tsv:
        month = 4
        tsv.write(tab_label + "\n")
        for year in range(2009, 2017):
            while month <= 12:
                # if the data is more recent than 2016-06, ignore
                if year >= 2016 and month > 6:
                    break
                month_s = str(month) if len(str(month)) == 2 else "0" + str(month)
                date = str(year) + "-" + month_s
                result = date
                for tag in tags:
                    if date in data[tag]:
                        result += "\t" + str(data[tag][date])
                    else:
                        result += "\t0"
                tsv.write(result + '\n')
                month += 1
            month = 1

