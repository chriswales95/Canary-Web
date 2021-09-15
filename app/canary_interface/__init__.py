from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, request, jsonify
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
    print(f"Working on {doc_id}")
    analysis = canary.analyse(doc)
    jobs[doc_id] = analysis
    print("Done")


@canary_interface.route('/analysis/<string:job_id>')
def get_result(job_id):
    try:
        job = jobs[str(job_id)]
        return jsonify(job), 200
    except:
        return job_id, 404
