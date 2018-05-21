from flask_table import Table, Col, LinkCol
from flask import url_for


class OpenJobs(Table):
    id = Col('id')
    pn = Col('Part Number')
    job = Col('Job Number')
    total_pcs = Col('Total pcs')
    rework = Col('Rework status')
    status = Col('Job status')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))

class Results(Table):
    id = Col('id')
    table = Col('Table #')
    status = Col('Status')
    pn = Col('Part Number')
    job = Col('Job Number')
    good_pcs = Col('Production output')
    rework = Col('Rework status')
    real_time_scans = Col('Real time production?')
    job_start_time = Col('Start Time')
    notes = Col('job notes')

