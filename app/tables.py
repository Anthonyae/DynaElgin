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
    id = Col('Id')
    table = Col(' Table # ')
    rework = Col(' Rework status ')
    real_time_scans = Col('Real time?')
    pn = Col(' Part Number ')
    job = Col('Job Number')
    good_pcs = Col('_Production output_ ')
    job_rate = Col("Rate(Pcs/Hour)")
    job_number_of_scans = Col("Number of scans")
    job_start_time = Col(' Start Time ')
    last_submit_time = Col(' Last Scan Time ')

    notes = Col(' Job notes ')
