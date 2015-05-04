# -*- coding: utf-8 -*-

def foo(*a, **kw):
    import pdb;pdb.set_trace()

@auth.requires_login()
def index():
#     db.project.project_id.represent = lambda v,r: (r.project_id and db.project._format % db.project[r.project_id].as_dict())

    fields = [db.project.title, db.project.status]
#     if 'project.project_id' in request.args:
#         fields += [db.project.project_id]
#         db.project.project_id.represent = lambda v: (v and db.project._format % db.project[v].as_dict())

    grid = SQLFORM.smartgrid(db.project,
        fields = fields,
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
        formname = 'project',
        breadcrumbs_class = 'breadcrumb'
    )

    if not grid.rows is None:
        def _replace(el):
            if 'projects' in el and  el.components[0] == T('projects'):
                el.components[0] = T("sub-projects")
            return el
        grid.elements('span', replace=_replace)

    return locals()
