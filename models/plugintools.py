# -*- coding: utf-8 -*-

link_repr = lambda v, *a: db.project._format % v

db.define_table('link_issue_project',
    Field('issue_id', 'reference issue', required=True, represent=link_repr),
    Field('project_id', 'reference project', required=True, represent=link_repr),
)

db.define_table('link_issue_issuegrp',
    Field('issue_id', 'reference issue', required=True, represent=link_repr),
    Field('issuegrp_id', 'reference issuegrp', required=True, represent=link_repr),
)

db.define_table('link_issuegrp_project',
    Field('issuegrp_id', 'reference issuegrp', required=True, represent=link_repr),
    Field('project_id', 'reference project', required=True, represent=link_repr),
)

def new_record(tablename):
    extras = dict([(k,v) for k,v in request.vars.items() if not k.startswith('_') and k not in db[tablename].fields])
    form = SQLFORM(db[tablename])
    if form.process(keepvalues=True).accepted:
        tabs = filter(lambda t: t._tablename.startswith('link_') and '%s_id' % tablename in t.fields and any([k in t.fields for k in extras.keys()]), db)
        if tabs:
            assert len(tabs)==1, "This should never happen, why it happens?"
            rec = dict([(k,int(v),) for k,v in extras.items()], **{'%s_id' % tablename: form.vars.id})
            tabs[0].insert(**rec)
    return dict(form=form)