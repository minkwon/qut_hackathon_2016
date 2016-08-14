import cPickle as pickle
reader = open("/Volumes/exFat/QUT_hack/indexed_list/tag_list.txt", "r")
writer = open("/Volumes/exFat/QUT_hack/indexed_list/tag_sorted_list", "wb")
lines = [line.rstrip('\n').split(" : ") for line in reader]
lines.sort(key=lambda pair: int(pair[1]), reverse=True)
pickle.dump(lines, writer)
reader.close()
writer.close()

