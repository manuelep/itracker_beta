# -*- coding: utf-8 -*-

def index():
    grid = SQLFORM.smartgrid(db.project,
        linked_tables = ['project'],
        csv = False,
        selectable = [
            ('New task/milestone', lambda ids : redirect(URL('issuegrp', 'new', vars=dict(project_id=ids)))),
            ('New issue', lambda ids : redirect(URL('issue', 'new', vars=dict(project_id=ids)))),
            #('button label2',lambda ...)
        ],
        formname = 'project'
    )
    return locals()
