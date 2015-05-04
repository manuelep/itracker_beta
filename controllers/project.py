# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    grid = SQLFORM.smartgrid(db.project,
        linked_tables = ['project'],
        selectable = [
            ('New task/milestone',
                lambda ids : redirect(
                    URL(
                        'issuegrp', 'index.html',
                        args = ('new', 'issuegrp',),
                        vars = dict(project_ids=ids),
                        user_signature = True
                    )
                )
            ),
            ('New issue',
                lambda ids : redirect(
                    URL(
                        'issue', 'index.html',
                        args = ('new', 'issue',),
                        vars = dict(project_ids=ids),
                        user_signature = True
                    )
                )
            ),
            #('button label2',lambda ...)
        ],
        csv = False,
        formname = 'project'
    )
    return locals()
