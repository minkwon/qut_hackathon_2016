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
        elif event == "end" and elem.tag == "row":
            parse_question(question_dict, elem)
            # everytime it parses one xml element, element data is freed
            root.clear()
            lineCount += 1
            if lineCount % 100000 == 0:
                print(lineCount)
                print_duration("A", start_time, lineCount)

    print_duration("Parsing", start_time)

    commit_questions_to_index(question_dict, writer, start_time)

    print_duration("Indexing", start_time)

# Example: { "2" : ( dateObj, "linux bash ubuntu", "31", [("31", dateObj), ("35", dateObj)] ) }
def parse_question(question_dict, elem):
    id = safe_get("Id", elem)
    creation_date_UTC = safe_get("CreationDate", elem)
    if creation_date_UTC is None:
        return
    question = True if safe_get("PostTypeId", elem) == "1" else False
    creation_date = dateutil.parser.parse(creation_date_UTC)

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

# assumes that datetime ordered by row ID
def commit_questions_to_index(question_dict, writer, start_time):
    questionCount = 0
    for row_id, data in question_dict.items():
        question_creation_date = data[0]
        tags = data[1]
        accepted_answer_id = data[2]
        answers = data[3]
        # continue if no answer received
        answer_accepted = None
        first_answer_received = None

        if len(answers) > 0:
            timedelta = answers[0][1] - question_creation_date
            first_answer_received = timedelta.days * 86400 + timedelta.seconds
            if accepted_answer_id is not None:
                for answer in answers:
                    if answer[0] == accepted_answer_id:
                        timedelta = answer[1] - question_creation_date
                        answer_accepted = timedelta.days * 86400 + timedelta.seconds

        # print("row " + row_id + " creation_date " + str(question_creation_date)
        #     + " first_answer " + str(first_answer_received) + " answer_accepted " + str(answer_accepted) + " " + tags)
        writer.add_document(id=row_id, creation_date=question_creation_date,
            first_answer_received=first_answer_received,
            answer_accepted=answer_accepted,
            tags=tags)
        questionCount += 1
        if questionCount % 100000 == 0:
            print(questionCount)
            print_duration("B", start_time, questionCount)

    # Overwriting the pre-existing index
    writer.commit(mergetype=writing.CLEAR)


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


def safe_get(attr, elem):
    return safe_decode(elem.attrib.get(attr))


def safe_decode(obj):
    # Python 2
    # return obj.decode("utf-8") if obj is not None else None

    # Python 3
    return obj if obj is not None else None

def print_duration(name, start_time, count=0):
    duration = datetime.datetime.now() - start_time

    if name == "A":
        total = 34857920
        speed = count / duration.seconds
        remaing_time = (total - count) / speed
        print(str(duration.seconds) + " seconds, " + str(speed) + "rec/sec, " + str(remaing_time) + " seconds remaining", flush=True)
    elif name == "B":
        speed = count / duration.seconds
        print(str(duration.seconds) + " seconds, " + str(speed) + "Q/sec", flush=True)
    else:
        print(name + ": It took " + str(duration.seconds) + " seconds", flush=True)
