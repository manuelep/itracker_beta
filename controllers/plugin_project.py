# -*- coding: utf-8 -*-

response.menu += [(T('Customize project'), False, None, [
    (T(tn), False, URL('plugin_project', '_customize', args=(tn,)), []) \
        for tn in db.tables if tn.startswith('project_')
])]

@auth.requires_login()
def index():
    db.project.description.readable = 'view' in request.args or 'edit' in request.args
    grid = SQLFORM.smartgrid(db.project, csv = False)
    return locals()

@auth.requires_login()
def _customize():

    def customize():
        tabname = request.args(0)
        grid = SQLFORM.grid(db[tabname], args=request.args[:1], csv = False)
        return dict(grid=grid)

    return customize()
