import os, os.path
import sys
import xml.etree.cElementTree as ET
import dateutil.parser
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import writing


def create_basic_index(index_name, schema, f):
    print("Creating index for " + index_name)
    start_time = datetime.datetime.now()

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir", schema=schema, indexname=index_name)
    # ix = whoosh.index.open_dir("indexdir", indexname="users")
    writer = ix.writer()

    context = ET.iterparse(f, events=("start", "end"))

    for event, elem in context:
        if event == "start":
            root = elem
        elif event == "end":
            write_document_to_index(elem, index_name, writer)
            # everytime it parses one xml element, element data is freed
            root.clear()
    # Overwriting the pre-existing index
    writer.commit(mergetype=writing.CLEAR)
    print_duration("Indexing", start_time)

# this will take up a lot of RAM
def create_question_index(schema, f):
    print("Creating index for Questions")
    start_time = datetime.datetime.now()

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir", schema=schema, indexname="questions")
    # ix = whoosh.index.open_dir("indexdir", indexname="users")
    writer = ix.writer()

    context = ET.iterparse(f, events=("start", "end"))
    
    lineCount = 0
    question_dict = {}

    for event, elem in context:
        if event == "start":
            root = elem
        elif event == "end":
            parse_question(question_dict, elem)
            # everytime it parses one xml element, element data is freed
            root.clear()
            lineCount += 1
            if lineCount % 100000 == 0:
                print(lineCount)
                print_duration("Parsing", start_time)


    print_duration("Parsing", start_time)

    commit_questions_to_index(question_dict, writer)

    print_duration("Indexing", start_time)

def parse_question(question_dict, elem):
    id = safe_get("Id", elem)
    question = True if safe_get("PostTypeId", elem) == "1" else False
    creation_date = dateutil.parser.parse(safe_get("CreationDate", elem))
    
    # question
    if question:
        tags = safe_get("Tags", elem)
        if tags is not None:
            tags = tags[1:-1].replace("><", " ")
        
        accepted_answer_id = safe_get("AcceptedAnswerId", elem)
        answers = []
        question_dict[id] = (creation_date, tags, accepted_answer_id, answers)
    
    # answer
    else:
        parent_id = safe_get("ParentId", elem)
        if parent_id is None:
            return

        if parent_id in question_dict:
            question_dict[parent_id][3].append((id, creation_date))

def commit_questions_to_index(question_dict, writer):
    for row_id, data in question_dict.items():
        # continue if no answer received
        if len(data[3]) == 0:
            continue

        sorted(data[3], key=lambda pair: pair[1])

        if data[2] is not None:
            # TODO: get timedelta in days or seconds for first question and accepted answer
        writer.add_document(id=row_id, creation_date=data[0],
            first_answer_received=first_answer_received,
            answer_accepted=answer_accepted,
            tags=data[1])
    # # Overwriting the pre-existing index
    # writer.commit(mergetype=writing.CLEAR)
    pass

def write_document_to_index(elem, index_name, writer):
    if elem.tag == "row":

        if index_name == "posts_test":

            row_id = safe_get("Id", elem)
            post_type = True if safe_get("PostTypeId", elem) == "1" else False
            parent_id = safe_get("ParentId", elem)
            tags = safe_get("Tags", elem)
            if tags is not None:
                tags = tags[1:-1].replace("><", " ")

            writer.add_document(id=row_id, post_type=post_type, parent_id=parent_id, tags=tags)

        elif index_name == "tags":

            id = safe_get("Id", elem)
            tag_name = safe_get("TagName", elem)
            count = safe_get("Count", elem)

            writer.add_document(id=id,
                                tag_name=tag_name,
                                count=count)

        elif index_name == "posts":

            id = safe_get("Id", elem)
            post_type = True if safe_get("PostTypeId", elem) == "1" else False
            parent_id = safe_get("ParentId", elem)
            accepted_answer_id = safe_get("AcceptedAnswerId", elem)
            tags = safe_get("Tags", elem)
            owner_id = safe_get("OwnerUserId", elem)
            score = safe_get("Score", elem)
            creation_date = dateutil.parser.parse(safe_get("CreationDate", elem))
            view_count = safe_get("ViewCount", elem)
            comment_count = safe_get("CommentCount", elem)
            answer_count = safe_get("AnswerCount", elem)
            favourite_count = safe_get("FavoriteCount", elem)
            title = safe_get("Title", elem)
            body = safe_get("Body", elem)

            if tags is not None:
                tags = tags[1:-1].replace("><", " ")

            writer.add_document(id=id,
                                post_type=post_type,
                                parent_id=parent_id,
                                accepted_answer_id=accepted_answer_id,
                                tags=tags,
                                owner_id=owner_id,
                                score=score,
                                creation_date=creation_date,
                                view_count=view_count,
                                comment_count=comment_count,
                                answer_count=answer_count,
                                favourite_count=favourite_count,
                                title=title,
                                body=body)

        # elif index_name == "questions":
        #     # id = Question id
        #     # creation_date = get_creation_date
        #     # first_answer_received = timedelta with earliest answer with parent to this
        #     # answer_accepted = timedelta with accepted answer''s create time
        #     # tags = get_tags
        #     writer.add_document()


def safe_get(attr, elem):
    return safe_decode(elem.attrib.get(attr))


def safe_decode(obj):
    # Python 2
    # return obj.decode("utf-8") if obj is not None else None
    
    # Python 3
    return obj if obj is not None else None

def print_duration(name, start_time):
    duration = datetime.datetime.now() - start_time
    print(name + ": It took " + str(duration.seconds) + "seconds", flush=True)

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

# questionSummed

tagSchema = Schema(id=ID(unique=True),
                   tag_name=ID(stored=True, unique=True),
                   count=NUMERIC(stored=True))

tagPostSchema = Schema(tag_name=ID(stored=True, unique=True),
                       count=NUMERIC(stored=True))

# create_basic_index("posts_test", postSchema, "H:/thesis/stackoverflow.com-Posts/posts_peek.xml")
create_question_index(questionSchema, "H:/thesis/stackoverflow.com-Posts/Posts.xml")