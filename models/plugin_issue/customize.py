# -*- coding: utf-8 -*-

response.menu += [(T('Customize issue'), False, None, [
    (T(tn), False, URL('plugin_issue', '_customize', args=(tn,)), []) \
        for tn in db.tables if tn.startswith('issue_')
])]

def customize():
    tabname = request.args(0)
    grid = SQLFORM.grid(db[tabname], args=request.args[:1], csv = False)
    return dict(grid=grid)