from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def search_field_scored(index, field, value):
    query = QueryParser(field, index.schema).parse(value)
    with index.searcher() as searcher:
        results = searcher.search(query)
        print results[0]


def print_all_docs(index):
    with index.reader() as reader:
        for doc in reader.all_stored_fields():
            print(str(doc))


def get_index(index_name):
    return open_dir("indexdir", indexname=index_name)


def search_keyword(field, value, index):
    with ix.searcher() as s:
        kwargs = {
            field: value
        }
        l = list(s.documents(**kwargs))
    return l

ix = get_index("posts_test")
print search_keyword("tags", u"linux", ix)