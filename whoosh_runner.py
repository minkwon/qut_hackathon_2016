from whoosh_index import *
from whoosh_search import *
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import writing

def create_topic_response_timeline_index(schema):
	questionIndex = get_index("questions")
	# topicResponseTimelineIndex = create_in("indexdir", schema=schema, indexname="topics_response_timeline")
	with questionIndex.reader() as reader:
		for doc in reader.all_stored_fields():
			print(str(doc))
		print("")
	return ""


postTest = Schema(id=ID(stored=True),
                  post_type=BOOLEAN(stored=True),
                  parent_id=ID(stored=True),
                  tags=KEYWORD(stored=True))

postSchema = Schema(id=ID(stored=True, unique=True),
                    post_type=BOOLEAN(stored=True),  # True if Question False if Answer
                    parent_id=ID(stored=True),
                    accepted_answer_id=ID(stored=True),
                    tags=KEYWORD(stored=True),
                    owner_id=ID(stored=True),
                    score=NUMERIC(stored=True),
                    creation_date=DATETIME(stored=True),
                    view_count=NUMERIC(stored=True),
                    comment_count=NUMERIC(stored=True),
                    answer_count=NUMERIC(stored=True),
                    favourite_count=NUMERIC(stored=True),
                    title=TEXT(stored=True),
                    body=TEXT(stored=True))

questionSchema = Schema(id=ID(stored=True, unique=True),
                        creation_date=DATETIME(stored=True),
                        first_answer_received=ID(stored=True),
                        answer_accepted=ID(stored=True),
                        tags=KEYWORD(stored=True),
                        )

topicResponseTimelineSchema = Schema(tag_name=ID(stored=True, unique=True),
									answer_accepted_timeline=STORED,
									first_question_received_timeline=STORED)


tagSchema = Schema(id=ID(unique=True),
                   tag_name=ID(stored=True, unique=True),
                   count=NUMERIC(stored=True))

# create_basic_index("posts_test", postSchema, "H:/thesis/stackoverflow.com-Posts/posts_peek.xml")
# create_question_index(questionSchema, "H:/thesis/stackoverflow.com-Posts/Posts.xml")

ix = get_index("posts_test")
with ix.reader() as reader:
	for doc in reader.all_stored_fields():
		print(doc.get('accepted_answer_id', 'not accepted'))
