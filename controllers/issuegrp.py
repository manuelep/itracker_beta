# -*- coding: utf-8 -*-

@auth.requires_login()
def index():

    if request.vars.project_id:
        sq = db(
            (db.issuegrp.id==db.link_issuegrp_project.issuegrp_id) & \
            (db.link_issuegrp_project.project_id==request.vars.project_id)
        )._select(db.issuegrp.id)
        query = db.issuegrp.id.belongs(sq)
    else:
        query = db.issuegrp.id>0

    grid = SQLFORM.grid(query,
        links = [
            dict(header='Projects', body=IssuegrpGrid.prj_link),
            dict(header='Wikis', body=IssuegrpGrid.doc_link),
        ],
        args = request.args,
        links_in_grid = False,
        oncreate = IssuegrpGrid.oncreate,
        csv = False,
        selectable = [
            ('New issue', lambda ids : redirect(URL('issue', 'new', vars=dict(issuegrp_id=ids)))),
            #('button label2',lambda ...)
        ],
        formname = 'issuegrp'
    )
    return dict(grid=grid)

@auth.requires_login()
def new():
    return new_record('issuegrp')
