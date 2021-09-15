from flask import Blueprint, render_template
from flask import abort

from app.canary_interface import jobs

frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static',
                     static_url_path='front/static')


@frontend.route('/')
def show():
    return render_template('index.html')


@frontend.route('/view/job/<string:job_id>')
def view(job_id):
    try:
        job = jobs[str(job_id)]
        import sadface
        sadface.sd = job
        import json
        return render_template(
            'job.html', job=job, dot=sadface.export_dot(),
            additional_head_elements=
            [
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js" integrity="sha512-vnRdmX8ZxbU+IhA2gLhZqXkX1neJISG10xy0iP0WauuClu3AIMknxyDjYHEpEhi8fTZPyOCWgqUCnEafDB/jVQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>',
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/full.render.js" integrity="sha512-1zKK2bG3QY2JaUPpfHZDUMe3dwBwFdCDwXQ01GrKSd+/l0hqPbF+aak66zYPUZtn+o2JYi1mjXAqy5mW04v3iA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
            ]
        ), 200
    except:
        return abort(404)
