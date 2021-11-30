from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, request
import uuid
import canary

canary_interface = Blueprint('canary_interface', __name__)

jobs = {}

executor = ThreadPoolExecutor(max_workers=1)


@canary_interface.route('/analyse', methods=["POST"])
def analyse():
    if request.is_json is True:
        if 'document_text' in request.get_json():
            doc_id = str(uuid.uuid4())
            jobs[doc_id] = None
            executor.submit(process, doc_id, request.get_json()['document_text'])

            return str(doc_id), 200
    elif 'document_text' in request.form:
        doc_id = str(uuid.uuid4())
        jobs[doc_id] = None

        executor.submit(process, doc_id, request.form['document_text'])
        return str(doc_id), 200
    else:
        raise TypeError("...")


def process(doc_id, doc):
    """Process a job"""
    print(f"Working on {doc_id}")

    try:
        analysis = canary.analyse(doc)
        jobs[doc_id] = {'analysis': analysis, 'original_document': doc}
    except Exception as e:
        jobs[doc_id] = "ERROR"
