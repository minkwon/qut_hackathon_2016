import os, os.path
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer

schema = Schema(accountid=ID(stored=True),
                location=ID(stored=True),
                reputation=STORED)

if not os.path.exists("indexdir"):
	os.mkdir("indexdir")

ix = whoosh.index.create_in("indexdir", schema=schema, indexname="users")
# ix = whoosh.index.open_dir("indexdir", indexname="users")
writer = ix.writer()
writer.add_document(accountid=u"abcd", location=u"UQ", reputation=u"1")
writer.commit()