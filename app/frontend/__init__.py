from flask import Blueprint, render_template, redirect, url_for, flash, abort
import sadface

from app.canary_interface import jobs

frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static',
                     static_url_path='front/static')


@frontend.route('/')
def index():
    return render_template('index.html',
                           additional_footer_elements=['<script src="/front/static/js/form.js"></script>'])


@frontend.route('/view/job/<string:job_id>')
def view(job_id):
    if job_id in jobs.keys():
        job = jobs[job_id]

        if job is None:
            return render_template('waiting_page.html',
                                   key=job_id,
                                   additional_head_elements=['<meta http-equiv="refresh" content="10" />']), 200

        if type(job) is str and job == "ERROR":
            flash("Encountered an error when processing the document. "
                  "Try again or open an issue on our GitHub for support.", "error")
            return redirect(url_for('frontend.index'))

        sadface.sd = job['analysis']
        component_nodes = [n for n in job['analysis']['nodes'] if 'canary' in n['metadata']]
        claims = [n for n in component_nodes if n['metadata']['canary']['type'] == 'Claim']
        premises = [n for n in component_nodes if n['metadata']['canary']['type'] == 'Premise']
        major_claims = [n for n in component_nodes if n['metadata']['canary']['type'] == 'MajorClaim']

        return render_template(
            'job.html',
            job=job['analysis'],
            original_doc=job['original_document'],
            dot=sadface.export_dot(),
            claims=claims,
            major_claims=major_claims,
            premises=premises,
            additional_head_elements=
            [
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js" integrity="sha512-vnRdmX8ZxbU+IhA2gLhZqXkX1neJISG10xy0iP0WauuClu3AIMknxyDjYHEpEhi8fTZPyOCWgqUCnEafDB/jVQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>',
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/full.render.js" integrity="sha512-1zKK2bG3QY2JaUPpfHZDUMe3dwBwFdCDwXQ01GrKSd+/l0hqPbF+aak66zYPUZtn+o2JYi1mjXAqy5mW04v3iA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
            ]
        ), 200
    else:
        return abort(404)
