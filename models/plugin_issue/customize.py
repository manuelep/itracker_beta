# -*- coding: utf-8 -*-

# response.menu += [(SPAN(ICON("wrench"), " ", T('Customize issue'), _class="text-warning"), False, None, [
#     (T(tn), False, URL('plugin_issue', 'customize', args=(tn,)), []) \
#         for tn in db.tables if tn.startswith('issue_')
# ])]

def _customize():
    tabname = request.args(0)
    grid = SQLFORM.grid(db[tabname], args=request.args[:1], csv = False)
    return dict(grid=grid)