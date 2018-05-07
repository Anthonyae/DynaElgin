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
    pn = Col('Part Number')
    job = Col('Job Number')
    total_pcs = Col('Total pcs')
    rework = Col('Rework status')
    timestamp = Col('Start Time')

