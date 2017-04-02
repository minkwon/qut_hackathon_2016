import os, os.path
import xml.etree.cElementTree as ET
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import writing


# f = "/Volumes/exFat/data/Posts.xml"
file_location = "Posts_mock.xml"


def create_index_post(index_name, schema, f):
    print "Creating index for " + index_name
    start_time = datetime.datetime.now()

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir", schema=schema, indexname=index_name)
    # ix = whoosh.index.open_dir("indexdir", indexname="users")
    writer = ix.writer()

    context = ET.iterparse(f)
    for event, elem in context:
        write_document_to_index(elem, index_name, writer)
        # everytime it parses one xml element, element data is freed
        elem.clear()
    # Overwriting the pre-existing index
    writer.commit(mergetype=writing.CLEAR)
    duration = datetime.datetime.now() - start_time
    print "It took " + str(duration.seconds) + "seconds"


def write_document_to_index(elem, index_name, writer):
    if elem.tag == "row":

        if index_name == "posts_test":

            row_id = safe_get("Id", elem)
            post_type = True if safe_get("PostTypeId", elem) == "1" else False
            parent = safe_get("ParentId", elem)
            tags = safe_get("Tags", elem)
            if tags is not None:
                tags = tags[1:-1].replace("><", " ")

            writer.add_document(id=row_id, post_type=post_type, parent=parent, tags=tags)

        elif index_name == "tags":

            id = safe_get("Id", elem)
            tag_name = safe_get("TagName")
            count = safe_get("Count")

            writer.add_document(id=id,
                                tag_name=tag_name,
                                count=count)

        elif index_name == "posts":

            id = safe_get("Id", elem)
            post_type = True if safe_get("PostTypeId", elem) == "1" else False
            parent_id = safe_get("ParentId", elem)
            accepted_answer_id = safe_get("AcceptedAnswerId", elem)
            tags = safe_get("Tags", elem)
            owner_id = safe_get
            score = safe_get("Score", elem)
            creation_date = safe_get("CreationDate", elem)
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

        elif index_name == "questions":
            # id = Question id
            # creation_date = get_creation_date
            # first_answer_received = timedelta with earliest answer with parent to this
            # answer_accepted = timedelta with accepted answer''s create time
            # tags = get_tags
            writer.add_document()



def safe_get(attr, elem):
    return safe_decode(elem.attrib.get(attr))


def safe_decode(obj):
    return obj.decode("utf-8") if obj is not None else None


postTest = Schema(id=ID(stored=True),
                  post_type=BOOLEAN,
                  parent=ID(stored=True),
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

questionSummed

tagSchema = Schema(id=ID(unique=True),
                   tag_name=ID(stored=True, unique=True),
                   count=NUMERIC(stored=True))

tagPostSchema = Schema(tag_name=ID(stored=True, unique=True),
                       count=NUMERIC(stored=True))

create_index_post("posts_test", postTest, "Posts_mock.xml")
